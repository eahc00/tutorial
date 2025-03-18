import torch
import torch.nn as nn
import torch.nn.functional as F

import math
import copy

from tutorial.commons import clones


class Conv1D(nn.Module):
    def __init__(self, nx, nf):
        super().__init__()
        self.nf = nf
        w = torch.empty(nx, nf)
        nn.init.normal_(w, std=0.02)
        self.weight = nn.Parameter(w)
        self.bias = nn.Parameter(torch.zeros(nf))

    def forward(self, x):
        # [B, S, dim_x] -> [B, S, dim_nf]
        size_out = x.size()[:-1] + (self.nf,)
        x = torch.addmm(self.bias, x.view(-1, x.size(-1)), self.weight)
        x = x.view(*size_out)

        return x


def gelu_new(x):
    return (
        0.5
        * x
        * (
            1.0
            + torch.tanh(math.sqrt(2.0 / math.pi) * (x + 0.044715 * torch.pow(x, 3.0)))
        )
    )


class GPT2MLP(nn.Module):
    def __init__(self, d_model, nx, dropout):
        super().__init__()
        self.c_fc = Conv1D(d_model, nx)
        self.c_proj = Conv1D(nx, d_model)
        # self.act = F.gelu
        self.act = gelu_new  # <- to get exact same result of huggingface
        self.dropout = nn.Dropout(dropout)

    def forward(self, x):
        return self.dropout(self.c_proj(self.act(self.c_fc(x))))


class GPT2MLP_linear_version(nn.Module):
    # CONV1D equivalent Linear implementation
    # but, you cannot import huggingface weigths to this module.
    def __init__(self, d_model, dim_feedforward=2048, dropout=0.1):
        super(GPT2MLP, self).__init__()
        self.feedforward_1 = nn.Linear(d_model, dim_feedforward)
        self.act_function = nn.GELU()
        self.feedforward_2 = nn.Linear(dim_feedforward, d_model)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x):
        x = self.feedforward_1(x)
        x = self.act_function(x)
        x = self.feedforward_2(x)
        x = self.dropout(x)
        return x


class MultiHeadAttention(nn.Module):
    def __init__(self, d_model, n_head, bias=True):
        super().__init__()
        self.n_head = n_head
        self.d_model = d_model
        self.c_attn = Conv1D(d_model, d_model * 3)

        self.dropout = nn.Dropout(0.1)
        self.c_proj = Conv1D(d_model, d_model)

        # we assume d_v always equals d_k
        assert d_model % n_head == 0
        self.d_k = d_model // self.n_head  # ex) d_model = 512, num_head = 8

    def split_heads(self, x):
        new_shape = x.size()[:-1] + (self.n_head, self.d_k)
        x = x.view(*new_shape)
        return x.permute(0, 2, 1, 3)  # [B, heads, seq_len, d_k]

    def _attn(self, q, k, v, mask=None):
        scores = torch.matmul(q, k.transpose(-2, -1))
        scores = scores / math.sqrt(v.size(-1))  # scaling by root
        nd, ds = scores.size(-2), scores.size(-1)

        # masking
        if mask != None:
            # sum-method
            mask = (1.0 - mask) * -1e4
            scores = scores + mask

        scores = F.softmax(scores, dim=-1)
        scores = self.dropout(scores)
        outputs = torch.matmul(scores, v)
        return outputs, scores

    def merge_heads(self, x):
        x = x.permute(0, 2, 1, 3).contiguous()
        new_shape = x.size()[:-2] + (x.size(-2) * x.size(-1),)
        return x.view(*new_shape)

    def forward(self, x, attention_mask):
        x = self.c_attn(x)  # new 'x' shape - '[1, 3, 2304]'
        q, k, v = x.split(self.d_model, dim=2)
        q, k, v = self.split_heads(q), self.split_heads(k), self.split_heads(v)
        out, scores = self._attn(q, k, v, attention_mask)
        out = self.merge_heads(out)
        out = self.c_proj(out)
        return out, scores


class GPT2_TransformerBlock(nn.Module):
    def __init__(self, d_model, n_head, dim_feedforward, dropout=0.1):
        super(GPT2_TransformerBlock, self).__init__()
        self.attn = MultiHeadAttention(d_model=d_model, n_head=n_head, bias=True)
        self.mlp = GPT2MLP(d_model=d_model, nx=dim_feedforward, dropout=dropout)
        self.ln_1 = nn.LayerNorm(d_model)
        self.ln_2 = nn.LayerNorm(d_model)

    def forward(self, x, look_ahead_mask):
        # Note : PRE Layer Normalization
        # Note : attention mask for GPT2 block is only look-ahead-mask
        # 1) layernorm and masked multihead
        nx = self.ln_1(x)
        a, attn_scores = self.attn(nx, attention_mask=look_ahead_mask)
        x = x + a

        # 2) layernorm and MLP
        m = self.mlp(self.ln_2(x))
        x = x + m

        return x, attn_scores


class GPT2Decoder(nn.Module):
    "Decoder Blcok of GPT2 - a stack of N layers"

    def __init__(self, num_layers, d_model, num_heads, dim_feedforward=None):
        super(GPT2Decoder, self).__init__()
        self.num_layers = num_layers
        if dim_feedforward == None:
            dim_feedforward = 4 * d_model

        a_layer = GPT2_TransformerBlock(
            d_model=d_model, n_head=num_heads, dim_feedforward=dim_feedforward
        )

        self.layers = clones(a_layer, self.num_layers)

    def forward(self, x, look_ahead_mask=None):
        # x : [B, tar_seq_len, d_model]
        # enc_output : [B, src_seq_len, d_model]
        # look_ahead_mask :

        layers_attn_scores = []
        "Pass the input(and mask) through each layer in turn."
        for layer in self.layers:
            x, attn_scroes = layer(x, look_ahead_mask)
            layers_attn_scores.append(attn_scroes)

        return x, layers_attn_scores


class GPT2(nn.Module):
    """GPT2 model"""

    def __init__(
        self,
        vocab_size,
        num_layers,
        emb_dim,
        d_model,
        num_heads,
        max_seq_length,
    ):
        super().__init__()
        self.max_seq_len = max_seq_length
        self.dropout_rate = 0.1
        self.dim_feedforward = 4 * d_model

        self.tokens = 0

        # GPT INPUT PART ------------------------
        self.wte = nn.Embedding(vocab_size, emb_dim)  # input vocab size -> emb_dim
        self.wpe = nn.Embedding(self.max_seq_len, emb_dim)  # each position -> emb_dim
        self.emb_dropout = nn.Dropout(self.dropout_rate)
        # position_ids (1, len position emb) is contiguous in memory and exported when serialize
        self.register_buffer(
            "position_ids", torch.arange(self.max_seq_len).expand((1, -1))
        )

        # GPT TRANSFORMER PART -----------------------
        self.blocks = GPT2Decoder(
            num_layers=num_layers,
            d_model=d_model,
            num_heads=num_heads,
            dim_feedforward=self.dim_feedforward,
        )

        self.ln_f = nn.LayerNorm(d_model)

        # GPT OUTPUT PART --------------------
        # highly depend on the task
        # decoder head
        self.head = nn.Linear(emb_dim, vocab_size, bias=False)

    def forward(self, input_ids):
        B, seq_len = input_ids.size()
        assert (
            seq_len <= self.max_seq_len
        ), "Input sequence length exceed model's maximum input length"

        # ---- INPUT (EMBEDDING) PART -----
        token_embeddings = self.wte(input_ids)
        seq_length = input_ids.shape[1]
        position_ids = self.position_ids[:, :seq_length]
        position_embeddings = self.wpe(position_ids)
        x = self.emb_dropout(token_embeddings + position_embeddings)

        # ---- Transformer PART ------
        lookahead_mask = self.look_ahead_mask(seq_len).to(
            x.device
        )  # mask : head compatible form.
        x, layer_attn_scores = self.blocks(x, look_ahead_mask=lookahead_mask)
        x = self.ln_f(x)  # <- layer norm on the final tranformer block

        # --- OUTPUT PART -------------
        logits = self.head(x)

        return logits

    def look_ahead_mask(self, tgt_len: int) -> torch.FloatTensor:
        mask = torch.triu(torch.ones(tgt_len, tgt_len, dtype=torch.int), diagonal=1)
        mask = 1 - mask  # reverse
        return mask

    def cp_weight(self, src, tar, copy_bias=True, include_eps=False):
        assert tar.weight.size() == src.weight.size(), "Not compatible parameter size"
        tar.load_state_dict(src.state_dict())

        if include_eps:
            # in case of LayerNorm
            with torch.no_grad():
                tar.eps = src.eps

    def cp_gpt2_transformer_block_weights(self, src, tar):
        ## src: huggingface GPT2 - Transformer model
        ## tar: my GPT2 -model- core weights

        ## layer normalization at top transformer block
        self.cp_weight(src.transformer.ln_f, tar.ln_f, include_eps=True)

        ## layer weight
        for layer_num, src_block in enumerate(src.transformer.h):
            # <<< MultiHeadAttention (Conv1D's parameters) >>>
            self.cp_weight(
                src_block.attn.c_attn, tar.blocks.layers[layer_num].attn.c_attn
            )  # c_attn
            self.cp_weight(
                src_block.attn.c_proj, tar.blocks.layers[layer_num].attn.c_proj
            )  # c_proj

            # same dropout for attention, residual and others
            # tar.blocks.layers[layer_num].attn.dropout.load_state_dict(src_block.attn_dropout)

            # <<< MLP >>>
            self.cp_weight(
                src_block.mlp.c_fc, tar.blocks.layers[layer_num].mlp.c_fc
            )  # c_fc
            self.cp_weight(
                src_block.mlp.c_proj, tar.blocks.layers[layer_num].mlp.c_proj
            )  # c_proj
            # tar.blocks.layers[layer_num],mlp.dropout.load_state_dict(src_block.mlp.dropout) # dropout

            # layer normalization parameters
            self.cp_weight(
                src_block.ln_1, tar.blocks.layers[layer_num].ln_1, include_eps=True
            )  # ln_1
            self.cp_weight(
                src_block.ln_2, tar.blocks.layers[layer_num].ln_2, include_eps=True
            )  # ln_2

        return tar

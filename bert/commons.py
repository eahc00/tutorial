# - Scaled Dot-Product attention mechanism
# - Query Key Value attention
# - Multihead attention

import torch
import torch.nn as nn
import torch.nn.functional as F

import math


def scaled_dot_product_attention(
    q: torch.Tensor,
    k: torch.Tensor,
    v: torch.Tensor,
    mask: torch.Tensor = None,
    dropout: float = 0.1,
) -> torch.Tensor:
    """
    In here, we try to calculate all multi-heads attentions at once.
    So, we assumed that first dimension of q, k and v is B*num_heads=...
        q : expect [..., query_seq_len, d_k]
        k : expect [..., key_seq_len, d_k]
        v : expect [..., key_seq_len, d_v]
    mask : expect extened shaped [B, num_heads, query_seq_len, key_seq_len] 1.0 for attend elements, 0 for masking elements
    dropout : expect float value.
    """
    # for scaling
    d_k = k.size()[-1]
    attn = torch.matmul(q, k.transpose(-2, -1)) / math.sqrt(
        d_k
    )  # [B, num_heads, query_seq_length, key_seq_length]

    # masking
    if mask != None:
        inverted_mask = 1.0 - mask
        inverted_mask = inverted_mask.masked_fill(
            inverted_mask.bool(), torch.finfo(attn.dtype).min
        )
        attn = attn + inverted_mask

    # calculate softmax
    attention_weights = F.softmax(
        attn, dim=-1
    )  # over key dimension #[..., seq_len, d_k]

    # Original Paper didn't mention about dropout on attention weights.
    # But many working architectures use dropout on attentions
    # so, in here we will apply dropout on scores
    if type(dropout) == float:
        attention_weights = F.dropout(attention_weights, dropout)
    else:
        attention_weights = dropout(attention_weights)

    # blending
    output = torch.matmul(attention_weights, v)
    return output, attention_weights


class Attention(nn.Module):
    ## this Attention implementation is almost identical to original transformer paper.
    def __init__(self, d_model, num_heads, dropout=0.1, use_bias=True):
        super(Attention, self).__init__()
        assert d_model % num_heads == 0
        self.num_heads = num_heads

        # We assume d_v always equals d_k
        self.d_k = d_model // num_heads  # ex) d_model = 512, num_head = 8 --> d_k = 64
        self.d_v = d_model // num_heads  # ex) d_model = 512, num_head = 8 --> d_v = 64

        self.wq = nn.Linear(d_model, d_model, bias=use_bias)
        self.wk = nn.Linear(d_model, d_model, bias=use_bias)
        self.wv = nn.Linear(d_model, d_model, bias=use_bias)

        self.dropout = nn.Dropout(dropout)

        self.wo = nn.Linear(d_model, d_model, bias=use_bias)

    def split_heads(self, x, batch_size):
        # split the projected dimension
        # [B, seq_len, heads * d_k] --> [B, heads, seq_len, d_k]
        x = x.view(batch_size, -1, self.num_heads, self.d_k)
        x = x.transpose(1, 2).contiguous()
        return x

    def forward(self, query, key, value, mask=None):
        q = self.wq(query)  # d_k --> d_k * num_head
        k = self.wk(key)  # d_k --> d_k * num_head
        v = self.wv(value)  # d_k --> d_k * num_head

        # shape change to [B, heads, seq_len, d_k]
        _, qS = q.size()[0], q.size()[1]  # qS = query_seq_len
        B, S = k.size()[0], k.size()[1]  # S = key_seq_len

        q = self.split_heads(q, B)
        k = self.split_heads(k, B)
        v = self.split_heads(v, B)

        # scaled_attention = [..., query_seq_len, d_k]
        # attention_weights = [..., query_seq_len, key_seq_len]
        scaled_attention, attention_weights = scaled_dot_product_attention(
            q, k, v, mask, self.dropout
        )

        scaled_attention = scaled_attention.transpose(
            1, 2
        )  # to be [B, query_seq_len, num_heads, d_k]

        concat_attention = scaled_attention.reshape(
            B, qS, -1
        )  # to be [B, query_seq_len, (num_heads*d_k)=d_models]

        output = self.wo(concat_attention)

        # output : # [B, query_seq_len, d_model]
        # attention_weights = [B, num_heads, query_seq_len, key_seq_len]
        return output, attention_weights


class TransformerEncoderLayer(nn.Module):
    # - a single layer for Transformer-Encoder block
    # - This Encoder block is almost identical to original transformer block
    # - activation function is changed to RELU
    #   - (note that, recently RELU is frequently replaced as GELU)

    def __init__(self, d_model, num_head, dim_feedforward, dropout=0.1):
        super(TransformerEncoderLayer, self).__init__()
        self.dropout = dropout

        # self-attention
        self.self_attn = Attention(d_model, num_head, dropout)

        # MLP
        self.act_fc = nn.GELU()
        self.fc1 = nn.Linear(d_model, dim_feedforward)
        self.fc2 = nn.Linear(dim_feedforward, d_model)

        # LN for after attention and final
        self.self_attn_layer_norm = nn.LayerNorm(d_model)
        self.final_layer_norm = nn.LayerNorm(d_model)

    def forward(self, x, mask):
        # 1) self-multihead-attention with add & norm
        residual = x
        x, attn_scores = self.self_attn(query=x, key=x, value=x, mask=mask)
        x = F.dropout(x, self.dropout, training=self.training)
        x = residual + x
        x = self.self_attn_layer_norm(x)

        # 2) MLP with add & norm
        residual = x
        x = self.act_fc(self.fc1(x))
        x = F.dropout(x, self.dropout, training=self.training)
        x = self.fc2(x)
        x = F.dropout(x, self.dropout, training=self.training)
        x = residual + x
        x = self.final_layer_norm(x)

        # out : [batch_size, step_size=S, d_model]
        return x, attn_scores


import copy


def clones(module, N):
    "Produce N identical layers."
    return nn.ModuleList([copy.deepcopy(module) for _ in range(N)])


class TransformerEncoder(nn.Module):
    # Encoder Block - a stack of N layers
    # Exactly same as TransformerEncoder
    def __init__(self, num_layers, d_model, num_heads, dropout, dim_feedforward=None):
        super(TransformerEncoder, self).__init__()
        self.num_layers = num_layers
        if dim_feedforward == None:
            dim_feedforward = 4 * d_model

        a_layer = TransformerEncoderLayer(d_model, num_heads, dim_feedforward, dropout)

        self.layers = clones(a_layer, self.num_layers)

    def forward(self, x, mask=None):
        # x expects : [B, seq_len, d_model]
        layers_attn_scores = []

        "Pass the input (and mask) through each layer in turn."
        for layer in self.layers:
            x, attn_scores = layer(x, mask)
            layers_attn_scores.append(attn_scores)

        return x, layers_attn_scores


def cp_weight(src, tar, copy_bias=True, include_eps=False):
    assert tar.weight.size() == src.weight.size(), "Not compatible parameter size"
    tar.load_state_dict(src.state_dict())

    if include_eps:
        # in case of LayerNorm
        with torch.no_grad():
            tar.eps = src.eps


class BertEmbeddings(nn.Module):

    def __init__(
        self,
        vocab_size,
        hidden_size,
        pad_token_id,
        max_bert_length_size,
        layer_norm_eps,
        hidden_dropout_prob,
    ):
        super().__init__()
        self.word_embeddings = nn.Embedding(
            vocab_size, hidden_size, padding_idx=pad_token_id
        )
        self.position_embeddings = nn.Embedding(max_bert_length_size, hidden_size)
        self.token_type_embeddings = nn.Embedding(2, hidden_size)

        self.LayerNorm = nn.LayerNorm(hidden_size, eps=layer_norm_eps)
        self.dropout = nn.Dropout(hidden_dropout_prob)

        self.register_buffer(
            "position_ids",
            torch.arange(max_bert_length_size).expand((1, -1)),
            persistent=False,
        )
        self.register_buffer(
            "token_type_ids",
            torch.zeros(
                self.position_ids.size(),
                dtype=torch.long,
                device=self.position_ids.device,
            ),
            persistent=False,
        )

        self.position_embeddings_type = "absolute"

    def forward(
        self,
        input_ids=None,
        token_type_ids=None,
        position_ids=None,
        inputs_embeds=None,
        past_key_values_length=0,
    ):
        if input_ids is not None:
            input_shape = input_ids.size()
        else:
            input_shape = inputs_embeds.size()[:-1]

        seq_length = input_shape[1]

        if position_ids is None:
            position_ids = self.position_ids[
                :, past_key_values_length : seq_length + past_key_values_length
            ]

        if token_type_ids is None:
            if hasattr(self, "token_type_ids"):
                buffered_token_type_ids = self.token_type_ids[:, :seq_length]
                buffered_token_type_ids_expanded = buffered_token_type_ids.expand(
                    input_shape[0], seq_length
                )
                token_type_ids = buffered_token_type_ids_expanded
            else:
                token_type_ids = torch.zeros(
                    input_shape, dtype=torch.long, device=self.position_ids.device
                )

        if inputs_embeds is None:
            inputs_embeds = self.word_embeddings(input_ids)
        token_type_embeddings = self.token_type_embeddings(token_type_ids)

        embeddings = inputs_embeds + token_type_embeddings
        if self.position_embeddings_type == "absolute":
            position_embeddings = self.position_embeddings(position_ids)
            embeddings += position_embeddings
        embeddings = self.LayerNorm(embeddings)
        embeddings = self.dropout(embeddings)

        return embeddings


class BertPooler(nn.Module):
    def __init__(self, hidden_size):
        super().__init__()
        self.dense = nn.Linear(hidden_size, hidden_size)
        self.activation = nn.Tanh()

    def forward(self, hidden_states):
        first_token_tensor = hidden_states[:, 0]
        pooled_output = self.dense(first_token_tensor)
        pooled_output = self.activation(pooled_output)
        return pooled_output


class BERT_CONFIG:
    def __init__(
        self,
        vocab_size,
        padding_idx,
        max_seq_length,
        d_model,
        layer_norm_eps,
        emb_hidden_dropout,
        num_layers,
        num_heads,
        att_prob_dropout,
        dim_feedforward,
    ):

        # embedding
        self.vocab_size = vocab_size
        self.padding_idx = padding_idx
        self.max_seq_length = max_seq_length
        self.d_model = d_model
        self.layer_norm_eps = layer_norm_eps
        self.emb_hidden_dropout = emb_hidden_dropout

        # attention
        self.num_layers = num_layers
        self.num_heads = num_heads
        self.att_prob_dropout = att_prob_dropout
        self.dim_feedforward = dim_feedforward


class BERT(nn.Module):
    def __init__(self, config):
        super().__init__()

        ## [Embeddings]
        self.embeddings = BertEmbeddings(
            config.vocab_size,
            config.d_model,
            config.padding_idx,
            config.max_seq_length,
            config.layer_norm_eps,
            config.emb_hidden_dropout,
        )

        ## [Transformers]
        self.encoder = TransformerEncoder(
            num_layers=config.num_layers,
            d_model=config.d_model,
            num_heads=config.num_heads,
            dropout=config.att_prob_dropout,
            dim_feedforward=config.dim_feedforward,
        )

        ## [Pooler]
        self.pooler = BertPooler(config.d_model)

    def forward(self, input_ids, attention_mask, token_type_ids=None):
        attention_mask = attention_mask[:, None, None, :]  # [B, 1, 1, seq_len]
        seq_embs = self.embeddings(input_ids, token_type_ids)
        output = self.encoder(seq_embs, attention_mask)
        pooled_out = self.pooler(output[0])

        layer_attention_scores = output[1]
        return pooled_out, layer_attention_scores

    def cp_encoder_block_weights_from_huggingface(self, src_encoder, tar_encoder):
        ## src: huggingface BERT model
        ## tar : my BERT model
        for layer_num, src_layer in enumerate(src_encoder.layer):
            # <<< to MultiHeadAttention (wq, wk, wv, wo) >>>
            cp_weight(
                src_layer.attention.self.query,
                tar_encoder.layers[layer_num].self_attn.wq,
            )
            cp_weight(
                src_layer.attention.self.key, tar_encoder.layers[layer_num].self_attn.wk
            )
            cp_weight(
                src_layer.attention.self.value,
                tar_encoder.layers[layer_num].self_attn.wv,
            )
            cp_weight(
                src_layer.attention.output.dense,
                tar_encoder.layers[layer_num].self_attn.wo,
            )

            # <<< to MLP (fc1, fc2) >>>
            cp_weight(
                src_layer.intermediate.dense, tar_encoder.layers[layer_num].fc1
            )  # feed_forward_1
            cp_weight(
                src_layer.output.dense, tar_encoder.layers[layer_num].fc2
            )  # feed_forward_2

            # layer normalization parameters
            cp_weight(
                src_layer.attention.output.LayerNorm,
                tar_encoder.layers[layer_num].self_attn_layer_norm,
                include_eps=True,
            )  # norm_1
            cp_weight(
                src_layer.output.LayerNorm,
                tar_encoder.layers[layer_num].final_layer_norm,
                include_eps=True,
            )  # norm_2

        return tar_encoder

    def copy_weights_from_huggingface(self, hg_bert):
        self.embeddings.load_state_dict(hg_bert.embeddings.state_dict())
        self.pooler.load_state_dict(hg_bert.pooler.state_dict())

        self.encoder = self.cp_encoder_block_weights_from_huggingface(
            src_encoder=hg_bert.encoder, tar_encoder=self.encoder
        )

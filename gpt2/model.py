import pytorch_lightning as pl
from transformers import GPT2Tokenizer, GPT2LMHeadModel, AdamW
from tutorial.gpt2.gpt2_model import GPT2
from tutorial.gpt2.utils import generate

import torch
from torch import nn
import evaluate
import bert_score
import pandas as pd


class Model(pl.LightningModule):
    def __init__(self, model_name, lr: float = 1e-5):
        super().__init__()
        self.save_hyperparameters()

        self.tokenizer = GPT2Tokenizer.from_pretrained(model_name)
        self.tokenizer.add_special_tokens(
            {"sep_token": "[SEP]", "pad_token": "[PAD]", "bos_token": "|beginoftext|"}
        )
        self.hg_model = GPT2LMHeadModel.from_pretrained(model_name)
        self.hg_model.resize_token_embeddings(len(self.tokenizer))

        self.lr = lr
        self.model = GPT2(
            vocab_size=len(self.tokenizer),
            num_layers=self.hg_model.config.n_layer,
            emb_dim=self.hg_model.config.n_embd,
            d_model=self.hg_model.config.n_embd,
            num_heads=self.hg_model.config.n_head,
            max_seq_length=self.hg_model.config.n_ctx,
        )
        self.model = self.model.cp_gpt2_transformer_block_weights(
            self.hg_model, self.model
        )

        self.model = self.hg_model

        self.loss_fct = nn.CrossEntropyLoss()

        self.bleu_scorer = evaluate.load("bleu")
        self.rougeL_scorer = evaluate.load("rouge")
        self.bert_scorer = bert_score.BERTScorer(lang="en", rescale_with_baseline=False)

        self.valid_preds, self.valid_targets = None, None
        self.test_preds, self.test_targets = None, None

    def forward(self, input_ids, labels=None):
        logits = self.model(input_ids=input_ids)
        loss = (
            self.loss_fct(logits.view(-1, logits.size(-1)), labels.view(-1))
            if labels != None
            else None
        )
        return {"logits": logits, "loss": loss}

    def training_step(self, batch, batch_idx):
        inputs = batch["input_ids"]  # [B, 512]
        labels = batch["label_ids"]  # [B, 512]

        outputs = self(inputs, labels=labels)
        # print(outputs["logits"].size()) # [B, 512, vocab_size]
        # print(outputs["logits"].argmax(dim=-1).size())  # [B, 512]

        loss = outputs["loss"]
        self.log(
            "train_loss", loss, on_step=True, on_epoch=True, prog_bar=True, logger=True
        )
        return loss

    def validation_step(self, batch, batch_idx):
        inputs = batch["input_ids"]
        labels = batch["label_ids"]

        outputs = self(inputs, labels=labels)
        loss = outputs["loss"]

        predicted_tokens = outputs["logits"].argmax(dim=-1)  # [B, 512]

        pred = self.tokenizer.decode(
            [token for token in predicted_tokens[0].tolist()],
            skip_special_tokens=True,
        )

        target = self.tokenizer.decode(
            [token for token in labels[0].tolist()],
            skip_special_tokens=True,
        )

        self.log("val_loss", loss, on_step=False, on_epoch=True, prog_bar=True)

        if self.valid_preds is None and self.valid_targets is None:
            self.valid_preds = [pred]
            self.valid_targets = [target]
        else:
            self.valid_preds.append(pred)
            self.valid_targets.append(target)

        return loss

    def on_validation_epoch_end(self):
        self.valid_preds, self.valid_targets = None, None

    def test_step(self, batch, batch_idx):
        inputs = batch["input_ids"]
        labels = batch["label_ids"]

        outputs = self(inputs, labels=labels)
        loss = outputs["loss"]

        predicted_tokens = outputs["logits"].argmax(dim=-1)  # [B, 512] (배치 크기: B)

        predicted_sentence = generate(self.model, self.tokenizer, inputs)
        # print(len(predicted_sentence))
        # print(predicted_sentence)

        sep_token_id = self.tokenizer.convert_tokens_to_ids("[SEP]")

        sep_idx = (labels == sep_token_id).nonzero(as_tuple=True)[0][0].item()
        target_text_ids = labels[:, sep_idx + 1 :]

        target_text = self.tokenizer.batch_decode(
            target_text_ids, skip_special_tokens=True
        )

        if self.test_preds == None and self.test_targets == None:
            self.test_targets = target_text
            self.test_preds = predicted_sentence
        else:
            self.test_targets.extend(target_text)
            self.test_preds.extend(predicted_sentence)

        return loss

    def on_test_epoch_end(self):
        logging_dict = self.compute_metrics(
            self.test_preds, self.test_targets, mode="test"
        )
        self.log_dict(logging_dict, on_epoch=True, prog_bar=True)
        self.result_output(self.test_preds)

    def result_output(
        self,
        test_preds,
        read_path="./resource/result-base.csv",
        output_path="./resource/result.csv",
    ):
        result_df = pd.read_csv(read_path)
        result_df["predicted_label"] = test_preds
        result_df.to_csv(output_path, index=False)

    def configure_optimizers(self):
        return AdamW(self.model.parameters(), lr=self.lr)

    def compute_metrics(self, preds, targets, mode):
        references_bleu = [[t] for t in targets]
        bleu1_result = self.bleu_scorer.compute(
            predictions=preds, references=references_bleu, max_order=1
        )["bleu"]
        bleu2_result = self.bleu_scorer.compute(
            predictions=preds, references=references_bleu, max_order=2
        )["bleu"]
        bleu3_result = self.bleu_scorer.compute(
            predictions=preds, references=references_bleu, max_order=3
        )["bleu"]
        bleu4_result = self.bleu_scorer.compute(
            predictions=preds, references=references_bleu, max_order=4
        )["bleu"]

        rouge_result = self.rougeL_scorer.compute(
            predictions=preds, references=targets
        )["rougeL"]

        _, _, bertscore_result = self.bert_scorer.score(preds, targets)

        return {
            f"{mode}_bleu1_score": bleu1_result,
            f"{mode}_bleu2_score": bleu2_result,
            f"{mode}_bleu3_score": bleu3_result,
            f"{mode}_bleu4_score": bleu4_result,
            f"{mode}_rouge_score": rouge_result,
            f"{mode}_bert_score": bertscore_result.mean().item(),
        }

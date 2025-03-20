import pytorch_lightning as pl
from transformers import GPT2Tokenizer, GPT2LMHeadModel, AdamW
from tutorial.gpt2.gpt2_model import GPT2
from tutorial.gpt2.utils import generate

from torch import nn
import evaluate
import bert_score
import pandas as pd


class Model(pl.LightningModule):
    def __init__(self, model_name, tokenizer, lr: float = 1e-5):
        super().__init__()
        self.save_hyperparameters()

        self.tokenizer = tokenizer
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

        self.loss_fct = nn.CrossEntropyLoss(ignore_index=-100)  # ignore_index 추가

        self.bleu_scorer = evaluate.load("bleu")
        self.rougeL_scorer = evaluate.load("rouge")
        self.bert_scorer = bert_score.BERTScorer(
            lang="en", rescale_with_baseline=False, device="cuda:3"
        )

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

        self.log("val_loss", loss, on_step=False, on_epoch=True, prog_bar=True)

        return loss

    def test_step(self, batch, batch_idx):
        input_ids = batch["input_ids"]  # shape: (B, seq_len)
        labels = batch["label_ids"]  # shape: (B, seq_len)

        outputs = self(input_ids, labels=labels)
        loss = outputs["loss"]

        # 배치 내 모든 샘플 별로 sep_idx 찾고, 각자 생성
        all_preds = []
        all_targets = []

        for i in range(input_ids.size(0)):  # B
            single_input = input_ids[i].unsqueeze(0)  # shape: (1, seq_len)
            single_label = labels[i].unsqueeze(0)  # shape: (1, seq_len)

            sep_positions = (
                single_input == self.tokenizer.convert_tokens_to_ids("<sep>")
            ).nonzero(as_tuple=True)

            sep_idx = sep_positions[1].item()  # 첫 번째 [SEP] 위치

            generated_sentence = generate(
                self.model,
                self.tokenizer,
                single_input[:, : sep_idx + 1],
                sep_idx,
            )
            # print(generated_sentence)

            target_text_ids = single_label[:, sep_idx + 1 :]
            target_text = self.tokenizer.batch_decode(
                [[id for id in seq if id != -100] for seq in target_text_ids],
                skip_special_tokens=True,
            )

            all_preds.extend(generated_sentence)
            all_targets.extend(target_text)

        if self.test_preds is None:
            self.test_preds = all_preds
            self.test_targets = all_targets
        else:
            self.test_preds.extend(all_preds)
            self.test_targets.extend(all_targets)

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

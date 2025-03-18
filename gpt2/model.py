import pytorch_lightning as pl
from transformers import GPT2Tokenizer, GPT2LMHeadModel, AdamW
from tutorial.gpt2.gpt2_model import GPT2

from torch import nn
import evaluate
import bert_score
import pandas as pd


class Model(pl.LightningModule):
    def __init__(self, model_name, lr: float = 1e-5):
        super().__init__()
        self.save_hyperparameters()

        self.tokenizer = GPT2Tokenizer.from_pretrained(model_name)
        self.tokenizer.add_special_tokens({"sep_token": "[SEP]", "pad_token": "[PAD]"})
        self.hg_model = GPT2LMHeadModel.from_pretrained(model_name)
        self.hg_model.resize_token_embeddings(len(self.tokenizer))

        self.lr = lr
        self.model = GPT2(
            vocab_size=self.hg_model.config.vocab_size + 2,
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
        self.bert_scorer = bert_score.BERTScorer(lang="en", rescale_with_baseline=False)

        self.valid_preds, self.valid_targets = None, None
        self.test_preds, self.test_targets = None, None

    def forward(self, input_ids, labels=None):
        logits = self.model(input_ids=input_ids)
        loss = self.compute_loss(logits, labels) if labels is not None else None
        return {"logits": logits, "loss": loss}

    def training_step(self, batch, batch_idx):
        inputs = batch["input_ids"]  # [B, 512]
        labels = batch["labels"]  # [B, 512]

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
        labels = batch["labels"]

        outputs = self(inputs, labels=labels)
        loss = outputs["loss"]

        predicted_tokens = outputs["logits"].argmax(dim=-1)  # [B, 512]

        pred = self.tokenizer.decode(
            [
                token
                for token in predicted_tokens[0].tolist()
                if token != self.tokenizer.pad_token_id
            ],
            skip_special_tokens=True,
        )

        target = self.tokenizer.decode(
            [token for token in labels[0].tolist() if token != -100],
            skip_special_tokens=True,
        )

        if self.valid_preds is None and self.valid_targets is None:
            self.valid_preds = [pred]
            self.valid_targets = [target]
        else:
            self.valid_preds.append(pred)
            self.valid_targets.append(target)

        return loss

    def on_validation_epoch_end(self):
        logging_dict = self.compute_metrics(
            self.valid_preds, self.valid_targets, mode="val"
        )
        self.log_dict(logging_dict, on_epoch=True, prog_bar=True)
        self.valid_preds, self.valid_targets = None, None

    def test_step(self, batch, batch_idx):
        inputs = batch["input_ids"]
        labels = batch["labels"]

        outputs = self(inputs, labels=labels)
        loss = outputs["loss"]

        predicted_tokens = outputs["logits"].argmax(dim=-1)  # [B, 512] (배치 크기: B)

        # 각 문장을 개별적으로 리스트에 저장
        preds = [
            self.tokenizer.decode(
                [
                    token
                    for token in predicted_tokens[i].tolist()
                    if token != self.tokenizer.pad_token_id
                ],
                skip_special_tokens=True,
            )
            for i in range(predicted_tokens.shape[0])  # 배치 내 모든 샘플 처리
        ]

        targets = [
            self.tokenizer.decode(
                [token for token in labels[i].tolist() if token != -100],
                skip_special_tokens=True,
            )
            for i in range(labels.shape[0])  # 배치 내 모든 샘플 처리
        ]

        # 리스트에 추가
        if self.test_preds is None and self.test_targets is None:
            self.test_preds = preds
            self.test_targets = targets
        else:
            self.test_preds.extend(preds)  # 리스트 확장 (배치 → 개별 샘플)
            self.test_targets.extend(targets)

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

    """shift 시켜야 다음 라벨 예측으로 동작하는 거 아닌가?? 왜 이 코드로는 학습이 제대로 안되고 밑에 그냥 logits 갖다 쓰면 학습이 되는지??"""
    # def compute_loss(self, logits, labels):
    #     shift_logits = logits[:, :-1, :].contiguous()
    #     shift_labels = labels[:, 1:].contiguous()

    #     loss = self.loss_fct(
    #         shift_logits.view(-1, shift_logits.size(-1)), shift_labels.view(-1)
    #     )
    #     return loss

    def compute_loss(self, logits, labels):
        logits = logits.contiguous()

        loss = self.loss_fct(logits.view(-1, logits.size(-1)), labels.view(-1))

        return loss

    def compute_metrics(self, preds, targets, mode):
        bleu1_list, bleu2_list, bleu3_list, bleu4_list = [], [], [], []
        rouge_list, bert_list = [], []

        for pred, target in zip(preds, targets):
            bleu1_result = self.bleu_scorer.compute(
                predictions=[pred], references=[[target]], max_order=1
            )["bleu"]
            bleu2_result = self.bleu_scorer.compute(
                predictions=[pred], references=[[target]], max_order=2
            )["bleu"]
            bleu3_result = self.bleu_scorer.compute(
                predictions=[pred], references=[[target]], max_order=3
            )["bleu"]
            bleu4_result = self.bleu_scorer.compute(
                predictions=[pred], references=[[target]], max_order=4
            )["bleu"]

            rouge_result = self.rougeL_scorer.compute(
                predictions=[pred], references=[target]
            )["rougeL"]

            _, _, bertscore_result = self.bert_scorer.score([pred], [target])

            bleu1_list.append(bleu1_result)
            bleu2_list.append(bleu2_result)
            bleu3_list.append(bleu3_result)
            bleu4_list.append(bleu4_result)
            rouge_list.append(rouge_result)
            bert_list.append(bertscore_result.mean().item())

        return {
            f"{mode}_bleu1_score": sum(bleu1_list) / len(bleu1_list),
            f"{mode}_bleu2_score": sum(bleu2_list) / len(bleu2_list),
            f"{mode}_bleu3_score": sum(bleu3_list) / len(bleu3_list),
            f"{mode}_bleu4_score": sum(bleu4_list) / len(bleu4_list),
            f"{mode}_rouge_score": sum(rouge_list) / len(rouge_list),
            f"{mode}_bert_score": sum(bert_list) / len(bert_list),
        }


import pandas as pd

from transformers import BertModel, AdamW
import pytorch_lightning as pl
from torch import nn
import torch

from commons import BERT
from dataset import YnatDataset

import evaluate

f1_score_metric = evaluate.load("f1")


def read_csv(path="./resource/result-base.csv"):
    return pd.read_csv(path)


class Model(pl.LightningModule):
    def __init__(
        self,
        model_name,
        bert_config,
        num_labels=7,
        lr: float = 1e-5,
    ):

        super().__init__()

        self.lr = lr
        self.bert_config = bert_config
        self.num_labels = num_labels

        self.model = BERT(bert_config)
        self.hg_model = BertModel.from_pretrained(model_name)

        self.model.copy_weights_from_huggingface(self.hg_model)
        self.fc = nn.Linear(self.bert_config.d_model, self.bert_config.d_model * 4)
        self.classifier = nn.Linear(self.bert_config.d_model * 4, num_labels)

        self.loss_fct = nn.CrossEntropyLoss()

        self.valid_pred, self.valid_target = None, None
        self.pred_labels, self.target_labels = None, None

    def forward(self, input_ids, attention_mask, labels):
        # attention_mask.shape = [8, 512]
        outputs = self.model(
            input_ids=input_ids, attention_mask=attention_mask
        )  ## (output, attention_score)
        output = self.fc(outputs[0])
        logits = self.classifier(output)

        loss = self.loss_fct(logits.view(-1, self.num_labels), labels.view(-1))

        return {"logits": logits, "loss": loss}

    def training_step(self, batch, batch_idx):
        inputs = batch
        outputs = self(inputs["input_ids"], inputs["attention_mask"], inputs["label"])

        loss = outputs["loss"]

        pred_label = torch.argmax(outputs["logits"], dim=1)
        metric = self.compute_metrics(
            pred_label.tolist(), inputs["label"].squeeze().tolist()
        )

        self.log_dict(
            {"train_loss": loss, "train_f1": metric},
            on_step=True,
            on_epoch=True,
            prog_bar=True,
        )

        return loss

    def validation_step(self, batch, batch_idx):
        inputs = batch
        outputs = self(inputs["input_ids"], inputs["attention_mask"], inputs["label"])
        loss = outputs["loss"]

        pred_label = torch.argmax(outputs["logits"], dim=1)
        target_label = inputs["label"].squeeze()

        metric = self.compute_metrics(pred_label.tolist(), target_label)

        self.log_dict(
            {"valid_loss": loss, "valid_f1": metric},
            on_step=False,
            on_epoch=True,
            prog_bar=True,
        )

        if self.valid_pred == None:
            self.valid_pred, self.valid_target = pred_label, target_label
        else:
            self.valid_pred = torch.cat([self.valid_pred, pred_label], dim=0)
            self.valid_target = torch.cat([self.valid_target, target_label], dim=0)

    def on_validation_epoch_end(self):
        metrics = self.compute_metrics(
            self.valid_pred.tolist(), self.valid_target.tolist()
        )

        self.log("valid_f1", metrics, on_step=False, on_epoch=True, logger=True)
        self.valid_pred, self.valid_target = None, None

    def test_step(self, batch, batch_idx):
        inputs = batch
        outputs = self(inputs["input_ids"], inputs["attention_mask"], inputs["label"])
        loss = outputs["loss"]

        pred_label = torch.argmax(outputs["logits"], dim=1)
        target_label = inputs["label"].squeeze()

        if self.pred_labels == None:
            self.pred_labels, self.target_labels = pred_label, target_label
        else:
            self.pred_labels = torch.cat([self.pred_labels, pred_label], dim=0)
            self.target_labels = torch.cat([self.target_labels, target_label], dim=0)

        return {"pred": pred_label, "target": target_label}

    def on_test_epoch_end(self):
        metrics = self.compute_metrics(
            self.pred_labels.tolist(), self.target_labels.tolist()
        )

        idx2label = {v: k for k, v in YnatDataset.label2idx.items()}

        result_df = read_csv()
        result_df["predicted_label"] = list(
            map(idx2label.get, self.pred_labels.tolist())
        )
        result_df["correct"] = (
            result_df["reference_label"] == result_df["predicted_label"]
        )

        result_df.to_csv("./result.csv", index=False)

        self.log("test_f1", metrics, on_step=False, on_epoch=True, logger=True)

    def compute_metrics(self, predictions, references):
        f1_result = f1_score_metric.compute(
            predictions=predictions,
            references=references,
            average="macro",
        )
        return f1_result["f1"]

    def configure_optimizers(self):
        optimizer = AdamW(self.parameters(), lr=self.lr)
        # optimizer = torch.optim.Adam(self.parameters(), lr=self.lr)
        return optimizer

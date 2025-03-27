from tutorial.commons import BERT

from transformers import BertModel

from transformers.optimization import Adafactor
from torch import nn

import pytorch_lightning as pl
import torch
from safetensors.torch import save_model

import evaluate

f1_score_metric = evaluate.load("f1")


class Model(pl.LightningModule):

    def __init__(self, model_name, tokenizer, bert_config, num_labels, lr=1e-5):
        super().__init__()

        self.model_name = model_name
        self.tokenizer = tokenizer
        self.bert_config = bert_config
        self.num_labels = num_labels
        self.lr = lr

        self.bert = BERT(bert_config)
        self.hg_model = BertModel.from_pretrained(model_name, add_pooling_layer=False)

        self.bert.copy_weights_from_huggingface(self.hg_model)

        self.classifier = nn.Linear(self.bert_config.d_model, num_labels)

        self.loss_fct = nn.CrossEntropyLoss(ignore_index=-100)

        self.valid_pred, self.valid_target = None, None
        self.test_pred, self.test_target = None, None

    def forward(self, input_ids, attention_mask, labels=None):
        # print(input_ids.size())  # [B, seq_len]
        outputs = self.bert(input_ids, attention_mask)
        # print(outputs[0].size())  # [B, seq_len, 768]
        logits = self.classifier(outputs[0])
        # print(logits.size())  # [B, seq_len, num_labels]
        # print(labels.size())  # [B, seq_len]
        if labels is not None:
            loss = self.loss_fct(logits.view(-1, self.num_labels), labels.view(-1))
        else:
            loss = None

        return {"logits": logits, "loss": loss}

    def training_step(self, batch, batch_idx):
        inputs = batch
        outputs = self(inputs["input_ids"], inputs["attention_mask"], inputs["label"])

        loss = outputs["loss"]
        pred_label = torch.argmax(outputs["logits"], dim=-1)
        metric = self.compute_metrics(
            pred_label.tolist(), inputs["label"].squeeze().tolist()
        )

        self.log_dict(
            {"train_loss": loss, "train_f1": metric},
            on_step=True,
            on_epoch=True,
            prog_bar=True,
        )

    def validation_step(self, batch, batch_idx):
        inputs = batch
        outputs = self(inputs["input_ids"], inputs["attention_mask"], inputs["label"])
        loss = outputs["loss"]

        pred_label = torch.argmax(outputs["logits"], dim=-1)
        target_label = inputs["label"].squeeze()

        metric = self.compute_metrics(pred_label.tolist(), target_label)

        self.log_dict(
            {"valid_loss": loss, "valid_f1": metric},
            on_step=False,
            on_epoch=True,
            prog_bar=True,
        )

        if self.valid_pred == None and self.valid_target == None:
            self.valid_pred, self.valid_target = pred_label, target_label
        else:
            self.valid_pred = torch.cat([self.valid_pred, pred_label])
            self.valid_target = torch.cat([self.valid_target, target_label])

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

        pred_label = torch.argmax(outputs["logits"], dim=-1)
        target_label = inputs["label"].squeeze()

        if self.test_pred == None and self.test_target == None:
            self.test_pred, self.test_target = pred_label, target_label
        else:
            self.test_pred = torch.cat([self.test_pred, pred_label])
            self.test_target = torch.cat([self.test_target, target_label])

    def on_test_epoch_end(self):
        metrics = self.compute_metrics(
            self.test_pred.tolist(), self.test_target.tolist()
        )

        save_model(self, "./ner_model.safetensors")

        self.log("test_f1", metrics, on_step=False, on_epoch=True, prog_bar=True)

    def compute_metrics(self, predictions, references):
        flat_predictions = [
            p
            for prediction, labels in zip(predictions, references)
            for p, l in zip(prediction, labels)
            if l != -100
        ]
        flat_true_labels = [l for label in references for l in label if l != -100]

        f1_result = f1_score_metric.compute(
            predictions=flat_predictions, references=flat_true_labels, average="macro"
        )

        return f1_result["f1"]

    def configure_optimizers(self):
        # optimizer = Adafactor(self.parameters())
        optimizer = torch.optim.Adam(self.parameters(), lr=self.lr)
        return optimizer

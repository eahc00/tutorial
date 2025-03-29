import csv
import os

from tutorial.practice1.utils import results_out, label2idx, idx2label

import torch
from tutorial.practice1.dataset import NERDataModule
from safetensors.torch import load_model

from tutorial.practice1.model import Model
from tutorial.commons import BERT_CONFIG
from transformers import BertConfig, BertTokenizerFast


class NERBERTInference:

    def __init__(self, model_name, num_labels):
        self.model_name = model_name
        self.tokenizer = BertTokenizerFast.from_pretrained(model_name)
        self.num_labels = num_labels

        hg_config = BertConfig.from_pretrained(model_name)

        my_config = BERT_CONFIG(
            vocab_size=self.tokenizer.vocab_size,
            padding_idx=self.tokenizer.convert_tokens_to_ids("[PAD]"),
            max_seq_length=hg_config.max_position_embeddings,
            d_model=hg_config.hidden_size,
            layer_norm_eps=hg_config.layer_norm_eps,
            emb_hidden_dropout=hg_config.hidden_dropout_prob,
            num_layers=hg_config.num_hidden_layers,
            num_heads=hg_config.num_attention_heads,
            att_prob_dropout=hg_config.attention_probs_dropout_prob,
            dim_feedforward=hg_config.intermediate_size,
            pooled_output=False,
        )

        self.model = Model(
            model_name=model_name,
            tokenizer=self.tokenizer,
            bert_config=my_config,
            num_labels=self.num_labels,
        )

        load_model(self.model, "/home/eahc00/tutorial/practice1/ner_model.safetensors")

    def ner_inference(self, inputs):
        words = inputs.split()

        encoded = self.tokenizer(
            words,
            is_split_into_words=True,
            return_tensors="pt",
            padding="max_length",
            truncation=True,
            max_length=512,
        )
        input_ids = encoded.input_ids
        attention_mask = encoded.attention_mask

        with torch.no_grad():
            outputs = self.model(input_ids, attention_mask)
            logits = outputs["logits"]

        predictions = torch.argmax(logits, dim=-1)

        word_ids = encoded.word_ids(batch_index=0)
        pred_labels = predictions[0].tolist()

        word_predictions = []
        previous_word_idx = None
        for idx, word_idx in enumerate(word_ids):
            if word_idx is None:
                continue
            if word_idx != previous_word_idx:
                word_predictions.append(pred_labels[idx])
                previous_word_idx = word_idx

        predicted_tags = [idx2label[label_idx] for label_idx in word_predictions]

        return words, predicted_tags


def main():
    model_name = "bert-base-multilingual-cased"
    num_labels = 29
    input_sentence = "관세청은 울산 경남 경북지역 등에 대규모 산불이 발생함에 따라 신속한 복구와 피해기업 지원을 위한 관세행정 종합지원방안을 수립해 추진한다고 26일 밝혔다."

    ner_bert_inference = NERBERTInference(model_name, num_labels)
    output = ner_bert_inference.ner_inference(input_sentence)
    print(output)


if __name__ == "__main__":
    main()

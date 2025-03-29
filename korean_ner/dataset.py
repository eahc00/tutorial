from Korpora import Korpora
from pytorch_lightning import LightningDataModule
from torch.utils.data import Dataset, DataLoader, random_split
import torch
import pandas as pd
import csv

from tutorial.korean_ner.utils import results_out


def load_data(path="/home/eahc00/tutorial/korean_ner/Korpora"):
    corpus = Korpora.load(
        "naver_changwon_ner", root_dir="/home/eahc00/tutorial/korean_ner/Korpora"
    )

    data = corpus.train

    tags = corpus.get_all_tags()
    tag_set = set()
    for tag in tags:
        tag = set(tag)
        tag_set.update(tag)

    labels = sorted(list(tag_set))
    label2idx = {label: idx for idx, label in enumerate(labels)}

    return data, label2idx


class NERDataset(Dataset):
    def __init__(self, item, label2idx, tokenizer, max_length):
        self.item = item
        self.label2idx = label2idx
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.item)

    def __getitem__(self, idx):
        words = self.item[idx].words
        ner_tags = self.item[idx].tags

        outputs = self.tokenizer(
            words,
            is_split_into_words=True,
            max_length=self.max_length,
            padding="max_length",
            truncation=True,
        )

        input_ids = outputs.input_ids
        attention_mask = outputs.attention_mask

        aligned_ner_tags = self._tokenize_and_align_labels(words, ner_tags)
        labels = [self.label2idx[ner_tag] for ner_tag in aligned_ner_tags]

        if len(labels) + 1 > self.max_length:
            labels = labels[: (self.max_length - 1)]

        adjusted_labels = (
            [-100] + labels + [-100] * (self.max_length - (len(aligned_ner_tags) + 1))
        )

        return {
            "input_ids": torch.tensor(input_ids),
            "attention_mask": torch.tensor(attention_mask),
            "label": torch.tensor(adjusted_labels),
        }

    def _tokenize_and_align_labels(self, words, ner_tags):

        labels = []

        for i in range(len(words)):
            subwords = self.tokenizer.tokenize(words[i])
            if ner_tags[i] == "-":
                labels.extend([ner_tags[i]] * len(subwords))
                continue
            tag, flag = ner_tags[i].split("_")
            if flag == "B":
                labels.append(f"{tag}_{flag}")
                labels.extend([f"{tag}_I"] * (len(subwords) - 1))
            else:
                labels.extend([ner_tags[i]] * len(subwords))

        return labels


class NERDataModule(LightningDataModule):
    def __init__(self, tokenizer, batch_size, max_length):
        super().__init__()

        self.tokenizer = tokenizer
        self.max_length = max_length
        self.batch_size = batch_size
        self.data, self.label2idx = load_data()

    def setup(self, stage="fit"):
        full_dataset = NERDataset(
            self.data, self.label2idx, self.tokenizer, self.max_length
        )

        generator = torch.Generator().manual_seed(42)
        self.train_dataset, self.valid_dataset, self.test_dataset = random_split(
            full_dataset, [0.8, 0.1, 0.1], generator=generator
        )

        self._save_test_data_to_csv()

    def train_dataloader(self):
        return DataLoader(
            self.train_dataset, batch_size=self.batch_size, shuffle=True, num_workers=4
        )

    def val_dataloader(self):
        return DataLoader(self.valid_dataset, batch_size=self.batch_size, num_workers=4)

    def test_dataloader(self):
        return DataLoader(self.test_dataset, batch_size=self.batch_size, num_workers=4)

    def _save_test_data_to_csv(self, file_path="test_base.csv"):
        if not hasattr(self, "test_dataset"):
            raise ValueError("You must run `setup()` before calling this function.")

        idx2label = {v: k for k, v in self.label2idx.items()}
        data_rows = []

        with open(file_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["sentence", "reference"])

            for original_idx in self.test_dataset.indices:
                item = self.data[original_idx]
                words = item.words
                tags = item.tags
                sentence = " ".join(words)
                tagged_sentence = results_out(words, tags)
                data_rows.append({"words": words, "tags": tags})

                writer.writerow([sentence, tagged_sentence])

        df = pd.DataFrame(data_rows)
        df.to_csv("test_words_and_tags.csv", index=False, encoding="utf-8")

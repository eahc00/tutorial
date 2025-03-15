from torch.utils.data import Dataset, DataLoader, random_split
import torch
import pytorch_lightning as pl

from transformers import BertTokenizer
import json


def load_json(file_path="/home/eahc00/tutorial/bert/ynat-v1.1/ynat-v1.1_train.json"):
    with open(file_path, "r") as file:
        data_json = json.load(file)

    return data_json


class YnatDataset(Dataset):

    label2idx = {
        "정치": 0,
        "경제": 1,
        "사회": 2,
        "생활문화": 3,
        "세계": 4,
        "IT과학": 5,
        "스포츠": 6,
    }

    def __init__(self, item, tokenizer, max_length):
        self.item = item
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.item)

    def __getitem__(self, index):
        title = self.item[index]["title"]
        inputs = self.tokenizer(
            title,
            max_length=self.max_length,
            padding="max_length",
            truncation=True,
            return_tensors="pt",
        )

        label = self.item[index]["label"]
        target = YnatDataset.label2idx[label]

        return {
            "input_ids": inputs["input_ids"].squeeze(0),
            "attention_mask": inputs["attention_mask"].squeeze(0),
            "label": torch.tensor(target, dtype=torch.long),
        }


class YnatDataloader(pl.LightningDataModule):
    def __init__(self, model_name, batch_size, max_length):
        super().__init__()
        self.batch_size = batch_size
        self.max_length = max_length
        self.tokenizer = BertTokenizer.from_pretrained(model_name)

    def setup(self, stage="fit"):
        ynat_dataset = load_json()
        ynat_test = load_json("/home/eahc00/tutorial/bert/ynat-v1.1/ynat-v1.1_dev.json")
        full_dataset = YnatDataset(ynat_dataset, self.tokenizer, self.max_length)

        train_size = int(len(ynat_dataset) * 0.8)
        self.train_dataset, self.valid_dataset = random_split(
            full_dataset, [train_size, len(ynat_dataset) - train_size]
        )

        self.test_dataset = YnatDataset(ynat_test, self.tokenizer, self.max_length)

    def train_dataloader(self):
        return DataLoader(
            self.train_dataset, batch_size=self.batch_size, shuffle=True, num_workers=4
        )

    def val_dataloader(self):
        return DataLoader(self.valid_dataset, batch_size=self.batch_size, num_workers=4)

    def test_dataloader(self):
        return DataLoader(self.test_dataset, batch_size=self.batch_size, num_workers=4)

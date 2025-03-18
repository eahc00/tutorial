from datasets import load_dataset
from torch.utils.data import Dataset, DataLoader
from transformers import GPT2Tokenizer

import pytorch_lightning as pl


class STSBDataset(Dataset):
    def __init__(self, item, tokenizer, max_length):
        self.item = item
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.item)

    def __getitem__(self, idx):
        sentence1 = self.item[idx]["sentence1"]
        sentence2 = self.item[idx]["sentence2"]

        inputs = self.tokenizer(
            sentence1 + "[SEP]" + sentence2,
            max_length=self.max_length,
            padding="max_length",
            truncation=True,
        )

        input_ids = inputs["input_ids"].squeeze(0)  # [512]

        labels = self.tokenizer(
            sentence1 + "[SEP]" + sentence2 + self.tokenizer.eos_token,
            max_length=self.max_length,
            padding="max_length",
            truncation=True,
            return_tensors="pt",
        )

        label_ids = labels["input_ids"].squeeze(0)

        sep_token_id = self.tokenizer.convert_tokens_to_ids("[SEP]")
        sep_idx = (input_ids == sep_token_id).nonzero(as_tuple=True)[0][0].item()
        pad_token_id = self.tokenizer.convert_tokens_to_ids("[PAD]")

        label_ids[: sep_idx + 1] = -100
        label_ids[label_ids == pad_token_id] = -100

        return {"input_ids": input_ids, "labels": label_ids}


class STSBDataloader(pl.LightningDataModule):
    def __init__(self, model_name, batch_size, max_length):
        super().__init__()
        self.batch_size = batch_size
        self.max_length = max_length
        self.tokenizer = GPT2Tokenizer.from_pretrained(model_name)
        self.tokenizer.add_special_tokens({"sep_token": "[SEP]", "pad_token": "[PAD]"})
        self.tokenizer.pad_token = "[PAD]"

    def setup(self, stage="fit"):

        train_dataset = load_dataset("nyu-mll/glue", "stsb", split="train")
        valid_dataset = load_dataset("nyu-mll/glue", "stsb", split="validation")
        test_dataset = load_dataset("nyu-mll/glue", "stsb", split="test")

        self.train_dataset = STSBDataset(train_dataset, self.tokenizer, self.max_length)
        self.valid_dataset = STSBDataset(valid_dataset, self.tokenizer, self.max_length)
        self.test_dataset = STSBDataset(test_dataset, self.tokenizer, self.max_length)

    def train_dataloader(self):
        return DataLoader(
            self.train_dataset, batch_size=self.batch_size, shuffle=True, num_workers=4
        )

    def val_dataloader(self):
        return DataLoader(self.valid_dataset, batch_size=self.batch_size, num_workers=4)

    def test_dataloader(self):
        return DataLoader(self.test_dataset, batch_size=self.batch_size, num_workers=4)

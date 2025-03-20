import pytorch_lightning as pl
from pytorch_lightning.callbacks import EarlyStopping
from transformers import GPT2Tokenizer

from tutorial.gpt2.dataset import STSBDataloader
from tutorial.gpt2.model import Model

max_length = 512
learning_rate = 1e-5
max_epoch = 30
batch_size = 16
model_name = "gpt2"
# seed = 42
gpu_id = [3]

# pl.seed_everything(seed)

tokenizer = GPT2Tokenizer.from_pretrained(model_name)
tokenizer.add_special_tokens(
    {
        "sep_token": "<sep>",
        "pad_token": "<pad>",
        "bos_token": "<|beginoftext|>",
        "eos_token": "<|endoftext|>",
    }
)

dataloader = STSBDataloader(tokenizer, batch_size, max_length)
dataloader.setup()

earlystopping_callback = EarlyStopping(monitor="val_loss", patience=2)

model = Model(model_name, tokenizer, lr=learning_rate)

trainer = pl.Trainer(
    accelerator="gpu",
    devices=gpu_id,
    max_epochs=max_epoch,
    callbacks=[earlystopping_callback],
)

trainer.fit(model=model, datamodule=dataloader)

model.eval()
trainer.test(model=model, datamodule=dataloader)

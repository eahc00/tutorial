import pytorch_lightning as pl
from pytorch_lightning.callbacks import EarlyStopping

from tutorial.gpt2.dataset import STSBDataloader
from tutorial.gpt2.model import Model

max_length = 512
learning_rate = 5e-5
max_epoch = 30
batch_size = 16
model_name = "gpt2"
seed = 42
gpu_id = "0,"

pl.seed_everything(seed)

dataloader = STSBDataloader(model_name, batch_size, max_length)
dataloader.setup()

earlystopping_callback = EarlyStopping(
    monitor="val_rouge_score", patience=2, mode="max"
)

model = Model(model_name, lr=learning_rate)

trainer = pl.Trainer(
    accelerator="gpu",
    devices=gpu_id,
    max_epochs=max_epoch,
    num_sanity_val_steps=0,
    callbacks=[earlystopping_callback],
)

trainer.fit(model=model, datamodule=dataloader)

model.eval()
trainer.test(model=model, datamodule=dataloader)

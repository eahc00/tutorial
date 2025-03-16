from tutorial.commons import BERT_CONFIG

from dataset import YnatDataset, YnatDataloader
from model import Model

from transformers import BertTokenizer, BertConfig
import pytorch_lightning as pl
from pytorch_lightning.callbacks import EarlyStopping

max_length = 512
learning_rate = 2e-5
max_epoch = 10
batch_size = 8
model_name = "bert-base-multilingual-cased"
gpu_id = "0,"

tokenizer = BertTokenizer.from_pretrained(model_name)
hg_config = BertConfig.from_pretrained(model_name)

my_config = BERT_CONFIG(
    vocab_size=tokenizer.vocab_size,
    padding_idx=tokenizer.convert_tokens_to_ids("[PAD]"),
    max_seq_length=hg_config.max_position_embeddings,
    d_model=hg_config.hidden_size,
    layer_norm_eps=hg_config.layer_norm_eps,
    emb_hidden_dropout=hg_config.hidden_dropout_prob,
    num_layers=hg_config.num_hidden_layers,
    num_heads=hg_config.num_attention_heads,
    att_prob_dropout=hg_config.attention_probs_dropout_prob,
    dim_feedforward=hg_config.intermediate_size,
)

print("dataloader setup start!!")
dataloader = YnatDataloader(model_name, batch_size, max_length)
dataloader.setup()
print("dataloader setup finish!!")

print("model and trainer!!")
model = Model(model_name, bert_config=my_config)

earlystopping_callback = EarlyStopping(monitor="valid_f1", patience=1, mode="max")

trainer = pl.Trainer(
    accelerator="gpu",
    devices=gpu_id,
    max_epochs=max_epoch,
    num_sanity_val_steps=0,
    callbacks=[earlystopping_callback],
)


print("training start!!")
trainer.fit(model=model, datamodule=dataloader)


print("Testing start!!")
model.eval()
trainer.test(model=model, datamodule=dataloader)

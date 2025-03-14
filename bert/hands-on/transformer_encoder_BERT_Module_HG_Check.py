import torch


def cli_main():

    from transformers import BertModel, BertTokenizer, BertConfig

    model_name = "bert-base-multilingual-cased"
    tokenizer = BertTokenizer.from_pretrained(model_name)
    hg_bert = BertModel.from_pretrained(model_name)
    hg_config = BertConfig.from_pretrained(model_name)

    from commons import BERT_CONFIG

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

    from commons import BERT

    my_bert = BERT(my_config)
    my_bert.copy_weights_from_huggingface(hg_bert)

    input_text = ["this is a test text", "is it working?"]

    tokenized_output = tokenizer(
        input_text, max_length=my_config.max_seq_length, padding="max_length"
    )

    input_ids = torch.tensor(tokenized_output.input_ids)
    o_attention_mask = torch.tensor(tokenized_output.attention_mask)
    token_type_ids = torch.tensor(tokenized_output.token_type_ids)

    with torch.no_grad():
        hg_bert.eval()
        hg_output = hg_bert(
            input_ids=input_ids,
            attention_mask=o_attention_mask,
            token_type_ids=token_type_ids,
        )

        my_bert.eval()
        my_output, my_layer_att_scores = my_bert(
            input_ids=input_ids,
            token_type_ids=token_type_ids,
            attention_mask=o_attention_mask,
        )

        print(hg_output.pooler_output)
        print("================")
        print(my_output)

        assert torch.all(
            torch.eq(hg_output.pooler_output, my_output)
        ), "Not same result!"

        print("\n\nSAME RESULT! -- Huggingface and My Code")


if __name__ == "__main__":
    cli_main()

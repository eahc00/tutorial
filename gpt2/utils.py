import torch.nn.functional as F
import torch


def top_k_top_p_filtering(
    logits: torch.Tensor,
    top_k: int = 0,
    top_p: float = 1.0,
    filter_value: float = -float("Inf"),
    min_tokens_to_keep: int = 1,
) -> torch.Tensor:
    """Top-K와 Nucleus (Top-P) 샘플링 적용"""

    if top_k > 0:
        top_k = min(
            max(top_k, min_tokens_to_keep), logits.size(-1)
        )  # 최소 토큰 개수 보장
        indices_to_remove = logits < torch.topk(logits, top_k)[0][..., -1, None]
        logits[indices_to_remove] = filter_value  # 낮은 확률 토큰 제거

    if top_p < 1.0:
        sorted_logits, sorted_indices = torch.sort(logits, descending=True)
        cumulative_probs = torch.cumsum(F.softmax(sorted_logits, dim=-1), dim=-1)

        sorted_indices_to_remove = cumulative_probs > top_p
        if min_tokens_to_keep > 1:
            sorted_indices_to_remove[..., :min_tokens_to_keep] = 0  # 최소 개수 유지
        sorted_indices_to_remove[..., 1:] = sorted_indices_to_remove[..., :-1].clone()
        sorted_indices_to_remove[..., 0] = 0

        indices_to_remove = sorted_indices_to_remove.scatter(
            1, sorted_indices, sorted_indices_to_remove
        )
        logits[indices_to_remove] = filter_value  # 선택된 토큰 제거
    return logits


def generate(
    model,
    tokenizer,
    input_ids,
    max_length=50,
    temperature=1.0,
    top_k=10,
    top_p=0.9,
):
    """GPT-2 모델을 사용하여 Autoregressive 방식으로 문장 생성"""

    model.eval()

    sep_token_id = tokenizer.convert_tokens_to_ids("[SEP]")
    pad_token_id = tokenizer.convert_tokens_to_ids("[PAD]")

    sep_idx = (input_ids == sep_token_id).nonzero(as_tuple=True)[0][0].item()
    input_ids = input_ids[:, : sep_idx + 1]
    # input_ids[sep_idx:] = pad_token_id

    generated_ids = input_ids.clone()

    for _ in range(max_length):
        with torch.no_grad():
            outputs = model(input_ids=generated_ids)
            logits = outputs[:, -1, :]

        filtered_logits = top_k_top_p_filtering(logits, top_k=top_k, top_p=top_p)
        probabilities = F.softmax(filtered_logits / temperature, dim=-1)
        next_token_id = torch.multinomial(probabilities, num_samples=1)
        # print(next_token_id.size()) # [B, 1]
        # print(generated_ids.size()) # [B, 512]

        # if (
        #     tokenizer.eos_token_id is not None
        #     and next_token_id == tokenizer.eos_token_id
        # ):
        #     break

        generated_ids = torch.cat([generated_ids, next_token_id], dim=-1)

    generated_ids = generated_ids[:, sep_idx + 1 :]  # [B, seq_len]
    generated_text = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)
    return generated_text

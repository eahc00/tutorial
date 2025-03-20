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
    sep_idx,
    max_length=50,
    temperature=1.0,
    top_k=50,
    top_p=0.98,
    n_gram_size=3,
):
    """GPT-2 모델을 사용하여 Autoregressive 방식으로 문장 생성"""

    model.eval()

    sep_token_id = tokenizer.convert_tokens_to_ids("<sep>")
    pad_token_id = tokenizer.convert_tokens_to_ids("<pad>")
    eos_token_id = tokenizer.convert_tokens_to_ids("|endoftext|")

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

        # print("next_token_id", next_token_id)

        if next_token_id.item() == eos_token_id or next_token_id.item() == pad_token_id:
            break

        generated_ids = torch.cat([generated_ids, next_token_id], dim=-1)
        # print(generated_ids)

    # generated_text = tokenizer.batch_decode(
    #     generated_ids[:, sep_idx + 1 :], skip_special_tokens=True
    # )
    generated_text = tokenizer.batch_decode(
        [[id for id in seq if id != -100] for seq in generated_ids[:, sep_idx + 1 :]],
        skip_special_tokens=True,
    )
    return generated_text


def prevent_ngram_repetition(generated_tokens, n):
    """생성된 문장에서 n-gram 반복을 방지하는 함수"""
    if len(generated_tokens) < n:
        return generated_tokens

    last_ngram = tuple(generated_tokens[-n:])
    count = generated_tokens[:-n].count(last_ngram)

    if count > 0:  # 동일한 n-gram이 이미 존재하면
        generated_tokens.pop()  # 마지막 토큰 제거

    return generated_tokens

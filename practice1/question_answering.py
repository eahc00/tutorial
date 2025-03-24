from dotenv import load_dotenv
import os

from transformers import pipeline
import torch
from pymilvus import connections, MilvusClient

from retrieval import (
    create_hybrid_request,
    search_hybrid_collection,
)

load_dotenv()
huggingface_token = os.environ.get("HUGGINGFACE_TOKEN")

conn = connections.connect(uri="./milvus.db")
client = MilvusClient("./milvus.db")


def retrieve_docs(query_text, collection_name, device):
    requests = create_hybrid_request(query_text, device)
    docs = search_hybrid_collection(collection_name, requests)

    return docs


def create_prompt(question, docs):
    system_prompt = """ 당신은 대학생의 학습을 도와주는 학습 도우미입니다.
    사용자가 물어보는 질문에 대한 답을 학생이 제공한 문서에서 찾아 제공합니다. 
    문서에 적힌 내용만을 답하고 없으면 문서에서 찾을 수 없는 내용이라고 대답하세요.
    존댓말로 친절하게 대답하여야 합니다. """

    user_text = (
        system_prompt + f"\n\n문서: {docs[0][0]['entity']['text']} \n\n질문: {question}"
    )

    messages = [{"role": "user", "content": user_text}]

    return messages


def answer_question(question, collection_name, device):
    docs = retrieve_docs(question, collection_name, device)
    subject = docs[0][0]["entity"]["subject"]

    model_pipe = pipeline(
        "text-generation",
        model="google/gemma-2-9b-it",
        device=device,
        torch_dtype=torch.bfloat16,
        token=huggingface_token,
    )

    prompt = create_prompt(question, docs)
    response = model_pipe(prompt, max_new_tokens=512)

    return f"과목 : {subject}\n" + response[0]["generated_text"][-1]["content"]


def main():
    device = "cuda:2" if torch.cuda.is_available() else "cpu"
    collection_name = "md_collection"

    ## ---------- NLP ------------ ##
    # question = "기존 RNN의 문제점은 무엇인가요?"
    # question = "S2S의 예시로는 뭐가 있나요?"
    # question = "표현학습이란 무엇인가요?"
    # question = "LSTM에 대해 설명해주세요"

    ## ---------- Network ------------ ##
    # question = "HTTP에 대해 설명해주세요"
    # question = "보안의 세 가지 목표가 무엇인가요?"
    # question = "NAT에 대해 자세히 설명해주세요"
    question = "ARP에 대해 자세히 설명해주세요"

    docs = retrieve_docs(question, collection_name, device)

    answer = answer_question(question, collection_name, device)
    print(answer)


if __name__ == "__main__":
    main()

from pymilvus import (
    connections,
    MilvusClient,
    utility,
    Collection,
    AnnSearchRequest,
    WeightedRanker,
)
from pymilvus.model.hybrid import BGEM3EmbeddingFunction

conn = connections.connect(uri="./milvus.db")
client = MilvusClient("./milvus.db")


def make_query_vector(query_text, device):
    bge_m3_ef = BGEM3EmbeddingFunction(use_fp16=False, device=device)
    query_embeddings = bge_m3_ef([query_text])

    dense_vector = query_embeddings["dense"][0]
    sparse_vector = query_embeddings["sparse"]

    return dense_vector, sparse_vector


def create_hybrid_request(query_text, device):
    dense_vector, sparse_vector = make_query_vector(query_text, device)

    dense_search_params = {
        "data": [dense_vector],
        "anns_field": "dense",
        "param": {"metric_type": "IP", "nprobe": 10},
        "limit": 2,
    }

    sparse_search_params = {
        "data": sparse_vector,
        "anns_field": "sparse",
        "param": {"metric_type": "IP"},
        "limit": 2,
    }

    requests = [
        AnnSearchRequest(**dense_search_params),
        AnnSearchRequest(**sparse_search_params),
    ]

    return requests


def search_hybrid_collection(collection_name, requests, limit=1):
    weighted_ranker = WeightedRanker(0.8, 0.3)
    results = client.hybrid_search(
        collection_name=collection_name,
        reqs=requests,
        ranker=weighted_ranker,
        limit=limit,
        output_fields=["subject", "text"],
    )

    return results


def main():
    collection_name = "md_collection"
    example_query = "기존 RNN의 문제가 무엇인가요?"
    requests = create_hybrid_request(example_query, device="cuda:2")
    res = search_hybrid_collection(collection_name, requests)

    print(res)


if __name__ == "__main__":
    main()

import os

from langchain_text_splitters import MarkdownHeaderTextSplitter
from pymilvus import (
    connections,
    MilvusClient,
    FieldSchema,
    CollectionSchema,
    DataType,
    Collection,
)
from pymilvus.model.hybrid import BGEM3EmbeddingFunction

connections.connect(uri="./milvus.db")
client = MilvusClient("./milvus.db")


def read_markdown(file_path):
    with open(file_path, "r") as f:
        docs = f.read()

    return docs


def chunk_docs(docs):
    header_to_split_on = [
        ("#", "header_1"),
        ("##", "header_2"),
        ("###", "header_3"),
        ("####", "header_4"),
    ]

    texts = []

    markdown_splitter = MarkdownHeaderTextSplitter(header_to_split_on)
    md_headers_splits = markdown_splitter.split_text(docs)
    for chunk in md_headers_splits:
        texts.append(chunk.page_content)

    return texts


def embedding_texts(texts, device, model_name="BAAI/bge-m3"):
    bge_m3_ef = BGEM3EmbeddingFunction(model_name, device=device, use_fp16=False)

    embeddings = bge_m3_ef(texts)
    dense_vectors = embeddings["dense"]
    sparse_vectors = embeddings["sparse"]

    return dense_vectors, sparse_vectors


def create_collections(collection_name, schema):
    if client.has_collection(collection_name):
        Collection(collection_name).drop()
    db_collection = Collection(collection_name, schema)

    sparse_index = {"index_type": "SPARSE_INVERTED_INDEX", "metric_type": "IP"}
    db_collection.create_index("sparse", sparse_index)
    dense_index = {"index_type": "AUTOINDEX", "metric_type": "IP"}
    db_collection.create_index("dense", dense_index)
    db_collection.load()

    return db_collection


def convert_coo_to_milvus_dict(sparse_coo):
    coo = sparse_coo.tocoo()
    return {int(idx): float(val) for idx, val in zip(coo.col, coo.data)}


def define_schema(dense_dim):
    fields = [
        FieldSchema(name="id", dtype=DataType.INT64, is_primary=True),
        FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=2048),
        FieldSchema(name="subject", dtype=DataType.VARCHAR, max_length=512),
        FieldSchema(name="dense", dtype=DataType.FLOAT_VECTOR, dim=dense_dim),
        FieldSchema(name="sparse", dtype=DataType.SPARSE_FLOAT_VECTOR),
    ]

    schema = CollectionSchema(fields=fields)

    return schema


def insert_data(collection_name, id, subject, text, dense_vectors, sparse_vectors):
    client.upsert(
        collection_name=collection_name,
        data={
            "id": id,
            "text": text,
            "subject": subject,
            "dense": dense_vectors,
            "sparse": convert_coo_to_milvus_dict(sparse_vectors),
        },
    )


def main():
    data_dir = "/home/eahc00/tutorial/practice1/md_data/"
    subject_names = os.listdir(data_dir)

    device = "cuda:2"
    dense_dim = 1024
    collection_name = "md_collection"

    schema = define_schema(dense_dim)
    create_collections(collection_name, schema)
    for subject_name in subject_names:
        file_names = os.listdir(os.path.join(data_dir, subject_name))
        for i, file_name in enumerate(file_names):
            file_path = os.path.join(data_dir, subject_name, file_name)
            docs = read_markdown(file_path)
            texts = chunk_docs(docs)
            dense_vectors, sparse_vectors = embedding_texts(texts, device)
            for j in range(len(texts)):
                insert_data(
                    collection_name=collection_name,
                    id=i * 100 + j,
                    subject=subject_name,
                    text=texts[j],
                    dense_vectors=dense_vectors[j],
                    sparse_vectors=sparse_vectors[j],
                )


if __name__ == "__main__":
    main()

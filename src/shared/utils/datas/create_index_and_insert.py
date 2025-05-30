import os

import fitz
import tiktoken
from dotenv import load_dotenv
from langchain.text_splitter import SpacyTextSplitter
from langchain_milvus import Milvus
from langchain_openai import OpenAIEmbeddings
from openai import OpenAI
from pymilvus import DataType, MilvusClient

load_dotenv("../.env")

lx3_path = "etc_files/LX3/LX3.pdf"
milvus_uri = "http://172.30.1.21:19530"
DIMENSION = 1536


def extract_text_from_pdf(path: str) -> str:
    docs = fitz.open(path)
    text = ""

    for page_num, page in enumerate(docs):
        text += page.get_text("text") + "\n"
    return text.strip()


def split_text(
    text: str, chunk_size: int, chunk_overlap: int, pipline="ko_core_news_sm"
) -> str:
    text_splitter = SpacyTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap, pipeline=pipline
    )
    return text_splitter.split_text(text)


def split_text_by_tokens(text, max_tokens=8192):
    encoding = tiktoken.get_encoding("cl100k_base")
    tokens = encoding.encode(text)

    chunks = []
    while len(tokens) > max_tokens:
        chunk = tokens[:max_tokens]
        chunks.append(chunk)
        tokens = tokens[max_tokens:]

    if len(tokens) > 0:
        chunks.append(tokens)
    return [encoding.decode(chunk) for chunk in chunks]


def generate_data_from_vectors(vectors: list, splitted_text: list[str]) -> list:

    data = [
        {"id": i, "vector": vectors[i], "text": splitted_text[i]}
        for i in range(len(splitted_text))
    ]
    return data


pdf_text = extract_text_from_pdf(path=lx3_path)
splitted_text = split_text(
    text=pdf_text, chunk_size=500, chunk_overlap=50, pipline="ko_core_news_sm"
)
# splitted_text = split_text(text=pdf_text)
# max_token 문제 8192 넘으면 안됨


print(len(splitted_text))

openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
vectors = []
for i in range(0, len(splitted_text)):
    batch = splitted_text[i]
    response = openai_client.embeddings.create(
        input=batch, model="text-embedding-3-small"
    )
    vectors.extend([vec.embedding for vec in response.data])


milvus_client = MilvusClient(uri=milvus_uri)
COLLECTION_NAME = "demo_collection"  # Milvus collection name
# Create a collection to store the vectors and text.
if milvus_client.has_collection(collection_name=COLLECTION_NAME):
    milvus_client.drop_collection(collection_name=COLLECTION_NAME)
milvus_client.create_collection(collection_name=COLLECTION_NAME, dimension=DIMENSION)

data = generate_data_from_vectors(vectors)
res = milvus_client.insert(collection_name="demo_collection", data=data)

print(res["insert_count"])
# embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")


"""
Milvus Usecase
"""

#
# vector_store = Milvus(
#     embedding_function=embeddings,
#     connection_args={"uri": milvus_uri},
#     # Set index_params if needed
#     # index_params={"index_type": "IVF_PQ", "metric_type": "COSINE"},
#     collection_name="incar_example_LX3",
# )
#
# client = MilvusClient(uri=milvus_uri)
#
# schema = client.create_schema(
#     auto_id=False,
#     # enable_dynamic_field=True,
# )
# schema.add_field(
#     field_name="pk", datatype=DataType.INT64, is_primary=True, auto_id=True
# )
# schema.add_field(field_name="vector", datatype=DataType.FLOAT_VECTOR, dim=1536)
# schema.add_field(field_name="text", datatype=DataType.JSON)
#
# client.create_collection(
#     collection_name="incar_example_LX3",
#     schema=schema,
# )
#
# index_params = client.prepare_index_params()
#
# index_params.add_index(
#     field_name="vector",
#     metric_type="COSINE",
#     index_type="IVF_FLAT",
#     index_name="vector_index",
#     params={"nlist": 128},
# )
# client.create_index(
#     collection_name="incar_example_LX3", index_params=index_params, sync=False
# )
#
# res = client.list_indexes(collection_name="incar_example_LX3")
# print(res)
#
# res = client.describe_index(
#     collection_name="incar_example_LX3", index_name="vector_index"
# )
# print(res)
#
# from langchain_core.documents import Document
#
# # embedding 모델과 분할된 documents 들을 벡터라이징후 벡터스토어에 삽입
# vector_store_saved = Milvus.from_documents(
#     splitted_documents,
#     embedding=embeddings,
#     collection_name="incar_example_LX3",
#     connection_args={"uri": milvus_uri},
# )

print("끝")

#

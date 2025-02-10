from langchain_community.document_loaders import PyMuPDFLoader
from langchain.text_splitter import SpacyTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv
from langchain_milvus import Milvus
from pymilvus import MilvusClient, DataType

load_dotenv()

embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")

milvus_uri = "http://172.30.1.21:19530"
vector_store = Milvus(
    embedding_function=embeddings,
    connection_args={"uri": milvus_uri},
    # Set index_params if needed
    # index_params={"index_type": "IVF_PQ", "metric_type": "COSINE"},
    collection_name="incar_example_LX3",
)

vector_store_loaded = Milvus(
    embedding_function=embeddings,
    connection_args={"uri": milvus_uri},
    collection_name="incar_example_LX3",
)

results = vector_store.similarity_search(
    query="차 문 어떻게 열어",
    k=2,
)

milvus_retrieval = vector_store.as_retriever()

results = milvus_retrieval.invoke("차문 어떻게 열어?")

print(results)

for res in results:
    print(f"* {res.page_content} [{res.metadata}]")

print("끝")

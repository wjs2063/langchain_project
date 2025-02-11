from langchain_community.document_loaders import PyMuPDFLoader
from langchain.text_splitter import SpacyTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv
from langchain_milvus import Milvus
from pymilvus import MilvusClient, DataType

load_dotenv("../.env")
loader = PyMuPDFLoader("etc_files/LX3/LX3.pdf")
documents = loader.load()

# print(len(documents))
# print(documents[0].page_content)

text_splitter = SpacyTextSplitter(
    chunk_size=1000, chunk_overlap=100, pipeline="ko_core_news_sm"
)
print("분할전 : ", len(documents))
# print("분할후 : ", len(splitted_documents))

splitted_documents = text_splitter.split_documents(documents)
embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")

"""
Chroma Usecase
"""

# chroma_db = Chroma(
#     persist_directory="./chroma_db",
#     embedding_function=embeddings,
# )
#
# chroma_db.add_documents(splitted_documents)

"""
Milvus Usecase
"""

milvus_uri = "http://172.30.1.21:19530"
vector_store = Milvus(
    embedding_function=embeddings,
    connection_args={"uri": milvus_uri},
    # Set index_params if needed
    # index_params={"index_type": "IVF_PQ", "metric_type": "COSINE"},
    collection_name="incar_example_LX3",
)

client = MilvusClient(uri=milvus_uri)

schema = client.create_schema(
    auto_id=False,
    # enable_dynamic_field=True,
)
schema.add_field(
    field_name="pk", datatype=DataType.INT64, is_primary=True, auto_id=True
)
schema.add_field(field_name="vector", datatype=DataType.FLOAT_VECTOR, dim=1536)
schema.add_field(field_name="text", datatype=DataType.JSON)

client.create_collection(
    collection_name="incar_example_LX3",
    schema=schema,
)

index_params = client.prepare_index_params()

index_params.add_index(
    field_name="vector",
    metric_type="COSINE",
    index_type="IVF_FLAT",
    index_name="vector_index",
    params={"nlist": 128},
)
client.create_index(
    collection_name="incar_example_LX3", index_params=index_params, sync=False
)

res = client.list_indexes(collection_name="incar_example_LX3")
print(res)

res = client.describe_index(
    collection_name="incar_example_LX3", index_name="vector_index"
)
print(res)

from langchain_core.documents import Document

# embedding 모델과 분할된 documents 들을 벡터라이징후 벡터스토어에 삽입
vector_store_saved = Milvus.from_documents(
    splitted_documents,
    embedding=embeddings,
    collection_name="incar_example_LX3",
    connection_args={"uri": milvus_uri},
)

print("끝")

#

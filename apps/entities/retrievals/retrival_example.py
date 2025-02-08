from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
import os
from dotenv import load_dotenv

load_dotenv()

embeddings = OpenAIEmbeddings(
    model="text-embedding-ada-002"
)

database = Chroma(
    persist_directory="../../datas/chroma_db",
    embedding_function=embeddings
)


documents = database.similarity_search("차 문 어떻게 열어?")

for document in documents:
    print("문서 내용 : ",document.page_content)
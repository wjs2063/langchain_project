from langchain.document_loaders import PyMuPDFLoader
from langchain.text_splitter import SpacyTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv

load_dotenv("../.env")
loader = PyMuPDFLoader("etc_files/LX3/LX3.pdf")
documents = loader.load()

# print(len(documents))
# print(documents[0].page_content)

text_splitter = SpacyTextSplitter(
    chunk_size=300,
    pipeline="ko_core_news_sm"
)
print("분할전 : ", len(documents))
# print("분할후 : ", len(splitted_documents))

splitted_documents = text_splitter.split_documents(documents)
embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
chroma_db = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embeddings,
)

chroma_db.add_documents(splitted_documents)

print("database 생성완료")

#

from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain_community.retrievers import WikipediaRetriever
from apps.entities.chat_models.chat_model_example import llm, HumanMessage
from apps.entities.retrievals.prompt import prompt
import os
from dotenv import load_dotenv

load_dotenv()

# query = "차 문 어떻게 열어?"
#
#
# # 단어나 문장의 의미를 포착하고
# embeddings = OpenAIEmbeddings(
#     model="text-embedding-ada-002"
# )
#
# database = Chroma(
#     persist_directory="../../datas/chroma_db",
#     embedding_function=embeddings
# )
#
# documents = database.similarity_search(query)
#
# documents_string = ""
# for document in documents:
#     #print("문서 내용 : ", document.page_content)
#     documents_string += f"""
# ---------------------------
# {document.page_content}
# """
#
# result = llm([
#     HumanMessage(content=prompt.format(document=documents_string, query=query)),
# ])

# print(result)


"""
retrieval QA 사용하기 with milvus | chroma
"""

query = "차 문 어떻게 열어?"
#
# # 단어나 문장의 의미를 포착하고
embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")

# database = Chroma(
#     persist_directory="../../datas/chroma_db",
#     embedding_function=embeddings
# )
from langchain_milvus import Milvus

milvus_uri = "http://172.30.1.21:19530"
database = Milvus(
    embedding_function=embeddings,
    connection_args={"uri": milvus_uri},
    # Set index_params if needed
    index_params={"index_type": "FLAT", "metric_type": "COSINE"},
    collection_name="incar_example_LX3",
)

documents = database.similarity_search(query)

retriever = database.as_retriever()

qa = RetrievalQA.from_llm(
    llm=llm,
    retriever=retriever,
    # doc_content_chars_max=10,
    # return_source_document=True,
)

result = qa(query)
print(result)


"""
Wikipedia retrieval example
"""

# wikipedia_retrieval = WikipediaRetriever(
#     wiki_client="wikipedia",
#     lang="ko",
#     doc_content_chars_max=300,
#     top_k_results=1,
# )
#
# documents = wikipedia_retrieval.get_relevant_documents("대구")
#
# print(documents)

from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain_community.retrievers import WikipediaRetriever
from apps.entities.chat_models.chat_model_example import HumanMessage
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

#
# # 단어나 문장의 의미를 포착하고
embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")

# database = Chroma(
#     persist_directory="../../datas/chroma_db",
#     embedding_function=embeddings
# )
from langchain_milvus import Milvus
from langchain_core.prompts import PromptTemplate

milvus_uri = "http://172.30.1.21:19530"
database = Milvus(
    embedding_function=embeddings,
    connection_args={"uri": milvus_uri},
    # Set index_params if needed
    index_params={"index_type": "FLAT", "metric_type": "COSINE"},
    collection_name="incar_example_LX3",
)

# documents = database.similarity_search(query)

retriever = database.as_retriever(
    search_kwargs={
        "k": 2,  # 최대 5개 문서 반환
        "score_threshold": 0.5,  # 유사도 0.8 이상만 포함
    }
)
prompt_template = """
You are an expert LX3 Car Assistant. Your role is to provide accurate and reliable answers based **only** on the provided context.  
You must **not generate information that is not present in the context**.  

### **Rules:**
1. **Always use only the given context** to answer the question. **Do not make up answers**.
2. Use words that closely match the terminology in the context.
3. **Answer in Korean**. Do not use other languages.  
4. If there are **multiple relevant pieces of information**, provide a structured and detailed response.

---

### **[검색된 문서]**  
{context}

---

### **[사용자 질문]**  
{question}

---

### **[LX3 어시스턴트의 답변]**

"""
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o", temperature=0.5)

prompt = PromptTemplate.from_template(template=prompt_template)
qa = RetrievalQA.from_llm(
    llm=llm,
    retriever=retriever,
    prompt=prompt,
    # doc_content_chars_max=10,
    return_source_documents=True,
    input_key="question",
    output_key="output",
    verbose=True,
)
# query = "넌 누구니"
# result = qa.invoke({"question": query})
# print(result)

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

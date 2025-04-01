from langchain_community.retrievers import WikipediaRetriever
from langchain_core.runnables import (
    RunnablePassthrough,
    RunnablePassthrough,
    RunnableParallel,
)
from apps.entities.chains.wikipedia_chain.prompt import prompt
from apps.entities.chat_models.chat_models import base_chat
import asyncio
from langchain_core.output_parsers import StrOutputParser

wiki_retriever = WikipediaRetriever(lang="en", doc_content_chars_max=500)


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


wikipedia_chain = (
    {"context": wiki_retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | base_chat
    #    | StrOutputParser()
)

# print(wikipedia_chain.invoke("tokyo"))
# asyncio.run(run_chain(ko_retriever, en_retriever, text="문재인"))
# RunnableParallel

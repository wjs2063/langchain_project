from langchain_community.retrievers import WikipediaRetriever

wikipedia_korea_retriever = WikipediaRetriever(
    wiki_client="wikipedia",
    lang="kr",
    doc_content_chars_max=500,
    top_k_results=1,
)

wikipedia_english_retriever = WikipediaRetriever(
    wiki_client="wikipedia",
    lang="en",
    doc_content_chars_max=500,
    top_k_results=1,
)
# print(wikipedia_english_retrieval.invoke("who is lee jae yong"))

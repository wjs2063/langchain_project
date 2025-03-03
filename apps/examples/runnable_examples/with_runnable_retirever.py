from langchain_community.retrievers import WikipediaRetriever
from langchain_community.tools import WikipediaQueryRun
from pydantic import BaseModel, Field
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_community.document_loaders import WikipediaLoader

api_wrapper = WikipediaAPIWrapper(
    wiki_client="wiki", top_k_results=2, doc_content_chars_max=100
)
wikipedia = WikipediaRetriever(top_k_results=2, doc_content_chars_max=100)

print(wikipedia.invoke("이재용이 누구야?"))


class WikiInputs(BaseModel):
    """Inputs to the wikipedia tool."""

    query: str = Field(
        description="query to look up in Wikipedia, should be full sentence"
    )


wiki_tool = WikipediaQueryRun(
    name="wiki-tool",
    description="look up things in wikipedia",
    args_schema=WikiInputs,
    api_wrapper=api_wrapper,
    return_direct=True,
)

docs = WikipediaLoader(query="이재용이 누구야", load_max_docs=2).load()


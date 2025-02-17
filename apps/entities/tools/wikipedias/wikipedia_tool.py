"""
https://python.langchain.com/v0.1/docs/modules/tools/
"""

from langchain_community.tools import WikipediaQueryRun
from langchain_community.document_loaders import WikipediaLoader
from langchain_community.utilities import WikipediaAPIWrapper
from pydantic import BaseModel, Field

api_wrapper = WikipediaAPIWrapper(
    wiki_client="wiki", top_k_results=2, doc_content_chars_max=100
)


# tool = WikipediaQueryRun(api_wrapper=api_wrapper)


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

# docs = WikipediaLoader(query="Doraemong", load_max_docs=2).load()

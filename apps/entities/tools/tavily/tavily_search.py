from langchain_community.tools.tavily_search import TavilySearchResults
from dotenv import load_dotenv

load_dotenv()
search = TavilySearchResults(max_results=2, verbose=True)

# search_results = search.invoke("What is the weather in Korea")
# print(search_results)
tavily_tools = [search]

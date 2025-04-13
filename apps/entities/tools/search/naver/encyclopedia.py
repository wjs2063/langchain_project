from langchain_core.runnables import RunnableLambda
import os
import aiohttp
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()


async def fetch_naver_search(query: str, display: int = 10) -> dict:
    """
    Fetches search results from the Naver Open API's encyclopedia search endpoint.

    This function sends an asynchronous GET request to the Naver search API and retrieves
    encyclopedia search results based on a specified query and the number of displayed results.
    It uses the credentials stored in the environment variables 'NAVER_SEARCH_CLIENT_ID' and
    'NAVER_SEARCH_CLIENT_SECRET' for authentication.

    Parameters
    ----------
    query: str
        The search query string to look up in the Naver encyclopedia API.
    display: int, optional
        The number of search results to display, default is 10.

    Returns
    -------
    dict
        The response body from the Naver search API in the format of a dictionary.

    Raises
    ------
    aiohttp.ClientError
        If there are any issues during the HTTP request.
    """
    url = f"https://openapi.naver.com/v1/search/encyc.json"
    client_id = os.getenv("NAVER_SEARCH_CLIENT_ID")
    client_secret = os.getenv("NAVER_SEARCH_CLIENT_SECRET")

    params = {"query": query, "display": display}

    headers = {
        "X-Naver-Client-Id": client_id,
        "X-Naver-Client-Secret": client_secret,
        "Content-Type": "application/json",
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, params=params) as response:
            rescode = response.status  # HTTP 응답 코드
            response_body = await response.text()  # 응답 데이터

            return response_body


async def run_naver_search(x) -> dict:
    """
    Performs an asynchronous Naver search using the provided query.

    This function accepts a dictionary containing a query string under the key
    'question' and performs an asynchronous search operation by invoking
    `fetch_naver_search`. It returns the search results in the form of a dictionary.

    Args:
        x (dict): Input dictionary containing the search query. Must include
        the key 'question' with a string value representing the search term.

    Returns:
        dict: The search results obtained from the Naver search.

    Raises:
        KeyError: If the input dictionary does not contain the 'question' key.
        Any exception raised by the `fetch_naver_search` call.
    """
    return await fetch_naver_search(query=x["question"])


naver_search_runnable = RunnableLambda(run_naver_search)

# asyncio.run(fetch_naver_search(query="겨울", display=5))

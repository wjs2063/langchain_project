import asyncio
import os
import sys
import urllib.parse
import urllib.request

import aiohttp
from aiohttp import ClientSession
from dotenv import load_dotenv
from langchain_core.tools import Tool, tool

# .env 파일 로드
load_dotenv()


async def fetch_naver_search(query: str, display: int = 10) -> dict:
    """
    Fetch data from Naver's open API for encyclopedia search.

    This function is used to query Naver's search API for retrieving
    encyclopedia search results. It sends an HTTP GET request with the
    provided query and the optional display count. API credentials are
    fetched from environment variables.

    Arguments:
        query: str
            The search query keyword to fetch results for.
        display: int, optional
            Number of search results to display. Defaults to 10.

    Returns:
        dict
            The HTTP response body parsed as a string.

    Raises:
        No documented raised exceptions.
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

            print(f"Response Code: {rescode}")
            print(response_body)
            return response_body


# 비동기 함수 실행
# asyncio.run(fetch_naver_search(query="겨울", display=5))

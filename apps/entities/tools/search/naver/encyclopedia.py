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
    NAVER 백과사전 검색을 통해서 해당 단어를 조회합니다.
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
asyncio.run(fetch_naver_search(query="겨울", display=5))

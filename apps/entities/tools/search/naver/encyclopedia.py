from langchain_core.tools import Tool, tool
from aiohttp import ClientSession
import os
import sys
import urllib.request
from dotenv import load_dotenv

load_dotenv()
# client_id = os.getenv("NAVER_SEARCH_CLIENT_ID")
# client_secret = os.getenv("NAVER_SEARCH_CLIENT_SECRET")
# query = "학교"
# params = {"query": query.encode("utf-8")}  # 딕셔너리 형태로 파라미터 생성
# encoded_params = urllib.parse.urlencode(params)  # URL 인코딩
# url = f"https://openapi.naver.com/v1/search/encyc.json?{encoded_params}&display=2"
# request = urllib.request.Request(url)
# request.add_header("X-Naver-Client-Id", client_id)
# request.add_header("X-Naver-Client-Secret", client_secret)
# request.add_header("Content-Type", "application/json")
# response = urllib.request.urlopen(request)
# rescode = response.getcode()
# if rescode == 200:
#     response_body = response.read()
#     print(response_body.decode("utf-8"))
# else:
#     print("Error Code:" + rescode)
import os
import asyncio
import aiohttp
import urllib.parse
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()


async def fetch_naver_search(query: str, display: int = 10):
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


# 비동기 함수 실행
# asyncio.run(fetch_naver_search(query="겨울", display=5))

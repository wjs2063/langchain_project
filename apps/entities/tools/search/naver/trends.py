import os
import sys
import urllib.request

from aiohttp import ClientSession
from dotenv import load_dotenv
from langchain_core.tools import Tool, tool

load_dotenv()

client_id = os.getenv("NAVER_SEARCH_CLIENT_ID")
client_secret = os.getenv("NAVER_SEARCH_CLIENT_SECRET")
url = "https://openapi.naver.com/v1/datalab/search"
body = '{"startDate":"2024-07-01","endDate":"2025-01-30","timeUnit":"month","keywordGroups":[{"groupName":"한글","keywords":["한글","korean"]},{"groupName":"영어","keywords":["영어","english"]}],"device":"pc","ages":["1","2"],"gender":"f"}'

request = urllib.request.Request(url)
request.add_header("X-Naver-Client-Id", client_id)
request.add_header("X-Naver-Client-Secret", client_secret)
request.add_header("Content-Type", "application/json")
response = urllib.request.urlopen(request, data=body.encode("utf-8"))
rescode = response.getcode()
if rescode == 200:
    response_body = response.read()
    print(response_body.decode("utf-8"))
else:
    print("Error Code:" + rescode)

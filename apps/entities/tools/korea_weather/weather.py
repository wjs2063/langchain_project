import os

from aiohttp import ClientSession
from dotenv import load_dotenv

load_dotenv()
url = "https://apihub.kma.go.kr/api/typ01/url/fct_shrt_reg.php?tmfc=0&authKey=_sjLTPuER0qIy0z7hGdKSg"

import json


async def call_weather_api(url: str):
    async with ClientSession(
        headers={
            "authKey": os.environ["KMA_API_KEY"],
        }
    ) as session:
        async with session.get(url) as resp:
            data = await resp.read()
            # response = await resp.json(content_type="text/plain;charset=euc-kr'")
            response = json.loads(data, encoding="cp949")
            print(response)
            return response


import asyncio


async def main():
    await call_weather_api(url=url)


asyncio.run(main())

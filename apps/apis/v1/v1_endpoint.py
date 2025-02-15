from fastapi import APIRouter, Request
from langchain.chat_models import init_chat_model
import os
from dotenv import load_dotenv
from chainlit.utils import mount_chainlit
from apps.entities.caches.caches import _redis_url
from redis.asyncio import Redis as aioredis

load_dotenv()
chat_router = APIRouter()


@chat_router.post("/chat")
async def chat_service(request: Request):
    return


@chat_router.get("/redis/flush")
async def flush_redis(request: Request):
    redis_client = await aioredis.from_url(_redis_url)
    await redis_client.flushall()
    return {"msg": "all key was flushed"}

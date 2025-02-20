from fastapi import APIRouter, Request
from langchain.chat_models import init_chat_model
import os
from dotenv import load_dotenv
from chainlit.utils import mount_chainlit
from apps.entities.caches.caches import _redis_url
from redis.asyncio import Redis as aioredis
from apps.apis.v1.chat.chat_endpoint import chat_router
from apps.apis.v1.auth.auth_endpoint import auth_router

load_dotenv()
v1_router = APIRouter()
v1_router.include_router(chat_router, prefix="/chat")
v1_router.include_router(auth_router, prefix="/auth")


@v1_router.get("/redis/flush")
async def flush_redis(request: Request):
    redis_client = await aioredis.from_url(_redis_url)
    await redis_client.flushall()
    return {"msg": "all key was flushed"}

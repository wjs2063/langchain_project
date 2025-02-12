from apps.entities.caches.caches import _redis_url
from langchain_community.chat_message_histories import RedisChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.cache import AsyncRedisCache
from langchain_core.messages import BaseMessage, message_to_dict, messages_from_dict
import json
from typing import Optional, Sequence
import asyncio
import redis.asyncio as redis


# class AsyncRedisChatMessageHistory(RedisChatMessageHistory):
#
#     def __init__(
#         self,
#         session_id: str,
#         redis_url: str = "redis://localhost:6379/0",
#         key_prefix: str = "message_store:",
#         buffer_size: int = 8,
#         ttl: Optional[int] = None,
#     ):
#         self.redis_client = redis.Redis.from_url(redis_url)
#         self.session_id = session_id
#         self.buffer_size = buffer_size
#         self.key_prefix = key_prefix
#         self.ttl = ttl
#
#     def add_message(self, message: BaseMessage) -> None:
#         """Append the message to the record in Redis"""
#         self.redis_client.lpush(self.key, json.dumps(message_to_dict(message)))
#         self.redis_client.ltrim(self.key, 0, self.buffer_size - 1)
#         if self.ttl:
#             self.redis_client.expire(self.key, self.ttl)


class SlidingWindowBufferRedisChatMessageHistory(RedisChatMessageHistory):

    def __init__(
        self,
        session_id: str,
        url: str,
        buffer_size: int = 8,
        key_prefix: str = "message_store:",
        ttl: Optional[int] = None,
    ):
        super().__init__(session_id, url, key_prefix=key_prefix, ttl=ttl)
        self.buffer_size = buffer_size

    def add_message(self, message: BaseMessage) -> None:
        """Append the message to the record in Redis"""
        self.redis_client.lpush(self.key, json.dumps(message_to_dict(message)))
        self.redis_client.ltrim(self.key, 0, self.buffer_size - 1)
        if self.ttl:
            self.redis_client.expire(self.key, self.ttl)


#
# history = AsyncRedisChatMessageHistory(
#     session_id="123", url=_redis_url, buffer_size=8
# )
#
#
# async def main():
#     messages = await history.aget_messages()
#     print(messages)
#
#
# import asyncio
#
# asyncio.run(main())

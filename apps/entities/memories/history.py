from apps.entities.caches.caches import _redis_url
from langchain_community.chat_message_histories import RedisChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.cache import AsyncRedisCache
from langchain_core.messages import BaseMessage, message_to_dict, messages_from_dict
import json
from typing import Optional, Sequence
import asyncio
import redis.asyncio as redis


# class AsyncRedisChatMessageHistory(BaseChatMessageHistory):
#
#     def __init__(
#             self,
#             session_id: str,
#             url: str = "redis://localhost:6379/0",
#             key_prefix: str = "message_store:",
#             buffer_size: int = 8,
#             ttl: Optional[int] = None,
#     ):
#         self.redis_client = redis.Redis.from_url(url)
#         self.session_id = session_id
#         self.buffer_size = buffer_size
#         self.key_prefix = key_prefix
#         self.ttl = ttl
#         self.loop = asyncio.new_event_loop()
#
#     @property
#     def key(self) -> str:
#         return self.key_prefix + self.session_id
#
#     @property
#     def messages(self):
#         return asyncio.run_coroutine_threadsafe(
#             self.aget_messages(), self.loop
#         ).result()
#
#     async def aget_messages(self) -> list[BaseMessage]:  # type: ignore
#         _items = await self.redis_client.lrange(self.key, 0, -1)
#         items = [json.loads(m.decode("utf-8")) for m in _items[::-1]]
#         messages = messages_from_dict(items)
#         return messages
#
#     def add_message(self, message: BaseMessage) -> None:
#         asyncio.run_coroutine_threadsafe(self.aadd_message(message), self.loop)
#
#     async def aadd_message(self, message: BaseMessage) -> None:
#         await self.redis_client.lpush(self.key, json.dumps(message_to_dict(message)))
#         await self.redis_client.ltrim(self.key, 0, self.buffer_size - 1)
#         if self.ttl:
#             await self.redis_client.expire(self.key, self.ttl)
#
#     def clear(self):
#         asyncio.run_coroutine_threadsafe(self.aclear(), self.loop)
#
#     async def aclear(self) -> None:
#         await self.redis_client.delete(self.key)


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

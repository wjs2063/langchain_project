import json
from typing import Optional, Sequence

from langchain_community.chat_message_histories import RedisChatMessageHistory
from langchain_core.messages import (BaseMessage, message_to_dict,
                                     messages_from_dict)

from apps.entities.caches.caches import _redis_url


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

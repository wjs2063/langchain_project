from langchain_core.runnables import RunnableBranch

from apps.entities.chat_models.chat_models import groq_chat, groq_deepseek
from apps.entities.chains.domain_selector_chain.prompt import selector_prompt
from apps.entities.memories.history import SlidingWindowBufferRedisChatMessageHistory
from apps.infras.redis._redis import _redis_url
import asyncio

domain_selector_chain = selector_prompt | groq_chat

buffered_memory = SlidingWindowBufferRedisChatMessageHistory(
    session_id="123", url=_redis_url, buffer_size=8
)

history = asyncio.run(buffered_memory.aget_messages())

# print(
#     domain_selector_chain.invoke(
#         {"chat_history": history, "query": "약속은 많은게 좋아 적은게 좋아??"}
#     )
#     .content.strip()
#     .lower()
# )
# d = (
#     domain_selector_chain.invoke(
#         {"chat_history": history, "query": "약속은 많은게 좋아 적은게 좋아??"}
#     )
#     .content.strip()
#     .lower()
# )

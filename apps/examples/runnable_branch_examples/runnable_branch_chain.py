from langchain_core.runnables import (
    RunnableBranch,
    RunnableLambda,
    RunnableParallel,
    RunnablePassthrough,
    RunnableMap,
)
from langchain_core.tracers import ConsoleCallbackHandler

from apps.entities.chains.schedule_chain.chain import schedule_agent
from apps.entities.chains.general_chat_chain.general_chain import general_chain
import asyncio
from apps.entities.memories.history import SlidingWindowBufferRedisChatMessageHistory
from apps.infras.redis._redis import _redis_url
from entities.chains.domain_selector_chain.domain_selector_chain import (
    domain_selector_chain,
)
from apps.entities.chains.domain_selector_chain.domain_selector_chain import (
    domain_selector_chain,
)

buffered_memory = SlidingWindowBufferRedisChatMessageHistory(
    session_id="123", url=_redis_url, buffer_size=8
)

# history = asyncio.run(buffered_memory.aget_messages())
runnable_chain_branch = RunnableLambda(
    lambda x: {
        **x,
        "domain": domain_selector_chain.invoke(x).content.strip().lower(),
    }  # 기존 input 유지 + "domain" 추가
) | RunnableBranch(
    (lambda x: x["domain"] == "schedule", schedule_agent),
    # (lambda x: x == "weather", "weather"),
    lambda x: general_chain,
)


# question = "3일후 일정 알려줘"
#
# print(
#     runnable_chain_branch.invoke(
#         {
#             "question": question,
#             "chat_history": history,
#         },
#         # config={"callbacks": [ConsoleCallbackHandler()]},
#     )
# )

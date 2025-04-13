from langchain_core.prompts import PromptTemplate
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

prompt = PromptTemplate(
    template="""
    당신은 {domain}초보자를 위한 AI 비서입니다. 사용자의 대답에 자세하고 친절한 설명을 해주세요
    사용자 질문 : {question}
    """,
    input_variables=["domain", "question"],
)

from langchain_openai import ChatOpenAI


base_chat = ChatOpenAI(model="gpt-4o", temperature=0.5, verbose=True)
chain = prompt | base_chat

# print(chain.invoke({"domain": "math", "question": "1 + 1 이 뭐야"}))


from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from datetime import datetime
from apps.entities.utils.time import get_current_time
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field


class Response(BaseModel):
    answer: str = Field(..., description="The answer text of the question.")
    detail: str = Field(
        ...,
        description="The detail text of the answer. reasonable evidence.  must be not empty",
    )


system_template = """
당신은 사용자의 친절한 AI학습 시스템입니다.  
사용자의 질문을 바탕으로 상세하고 친절한 응답을 반환하세요.  

"""

user_template = f"""
당신은 {{domain}} 에 특화된 멘토 시스템입니다.

"""

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_template),
        (
            "user",
            f"{user_template}\n\n#Format: {{format_instructions}}\n\n#Question: {{question}}",
        ),
    ]
)

output_parser = JsonOutputParser(pydantic_object=Response)

prompt = prompt.partial(format_instructions=output_parser.get_format_instructions())


chain = prompt | base_chat | output_parser

# print(chain.invoke({"domain": "math", "question": "1 + 1"}))

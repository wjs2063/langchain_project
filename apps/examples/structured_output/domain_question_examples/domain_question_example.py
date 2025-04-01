from langchain_core.output_parsers import JsonOutputParser
from langchain_core.tracers import ConsoleCallbackHandler

from entities.chains.general_chat_chain.general_chain import general_chain
from entities.chains.schedule_chain.chain import schedule_agent
from entities.chains.weather_chain.weather_chain import weather_agent
from entities.retrievals.wikipedia_retriever.wiki_retriever import (
    wikipedia_english_retriever,
    wikipedia_korea_retriever,
)
from pydantic import BaseModel, Field
from entities.chat_models.chat_models import base_chat
from langchain_core.runnables import (
    RunnableParallel,
    RunnablePassthrough,
    RunnableLambda,
    RunnableBranch,
)
from typing import List
from apps.examples.structured_output.domain_question_examples.prompt import prompt


class Question(BaseModel):
    domain: str = Field(
        ..., description="The domain of the question. rephrased question"
    )
    question: str = Field(..., description="The question text.")


class QuestionResponse(BaseModel):
    questions: List[Question] = Field(..., description="The list of Questions class")


domain_chains = {
    "weather": weather_agent,
    "schedule": schedule_agent,
    "general": general_chain,
}
import asyncio


async def create_dynamic_parallel_executor(data: dict):
    print(data)
    response = await asyncio.gather(
        *[
            domain_chains[item["domain"]].ainvoke({"question": item["question"]})
            for item in data["questions"]
        ]
    )
    return response


parser = JsonOutputParser(pydantic_object=QuestionResponse)

prompt = prompt.partial(format_instructions=parser.get_format_instructions())

chain = prompt | base_chat | parser

# response = chain.invoke(
#     {"question": "뉴턴이 누군지 알려주고 천호동 날씨나 알려줘"},
#     config={"callbacks": [ConsoleCallbackHandler()]},
# )
multi_domain_chain = chain | RunnableLambda(
    lambda x: asyncio.run(create_dynamic_parallel_executor(x))
)
# print(
#     a.invoke(
#         {"question": "3일후 스케쥴일정이랑 천호동 날씨나 알려줘"},
#         config={"callbacks": [ConsoleCallbackHandler()]},
#     )
# )


async def chain_run():
    result = await multi_domain_chain.ainvoke(
        {"question": "3일 후 스케줄 일정이랑 오늘 천호동 날씨나 알려줘"},
        config={"callbacks": [ConsoleCallbackHandler()]},
    )
    return result


# print(asyncio.run(chain_run()))
# print(
#     RunnableLambda(
#         lambda x: {k: v for item in x["questions"] for k, v in item.items()}
#     ).invoke(response)
# )

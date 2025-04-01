import asyncio
import time

from langchain.chains import LLMChain
from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from pydantic import BaseModel, Field

from apps.entities.chat_models.chat_models import base_chat


# Base LLM Chain Usage


class SimpleAnswer(BaseModel):
    summary: str = Field(description="summary")
    category: str = Field(description="category")
    answer: str = Field(description="answer")


response_schemas = [
    ResponseSchema(name="answer", description="answer of the user question"),
    ResponseSchema(name="summary", description="summary of the answer"),
    ResponseSchema(name="category", description="category of the user question"),
]
structured_output_parser = StructuredOutputParser.from_response_schemas(
    response_schemas
)

prompt = PromptTemplate(
    template="Answer the user question, Be answer korean language\n #format:{format_instructions}\n #question : {question} ",
    input_variables=["question"],
    partial_variables={
        "format_instructions": structured_output_parser.get_format_instructions()
    },
)

# chain = LLMChain(llm=base_chat, prompt=prompt)
chain = prompt | base_chat | structured_output_parser

# print(
#     {"question": "오늘의 날씨"}
#     | RunnablePassthrough.assign(output=lambda x: chain.invoke(x["question"]))
# )
# print(chain.invoke({"question": "오늘의 날씨"}))

# print(chain.invoke({"country": "한국"}))

# print(chain.predict(country="한국"))


"""
stream Usage
"""

"""
batch Usage
"""


async def chain_ainvoke(input_dict):
    print(f"ainvoke 콜 시작!, {input_dict}")
    return await chain.ainvoke(input_dict)


async def main(*args):
    start_time = time.time()
    responses = await asyncio.gather(
        *[
            chain_ainvoke(input_dict={"question": "한국"}),
            chain_ainvoke(input_dict={"question": "미국"}),
            chain_ainvoke(input_dict={"question": "중국"}),
            chain_ainvoke(input_dict={"question": "영국"}),
            chain_ainvoke(input_dict={"question": "필리핀"}),
            chain_ainvoke(input_dict={"question": "베트남"}),
        ]
    )
    end_time = time.time()
    print(end_time - start_time)
    for response in responses:
        print(response)
    return response


# asyncio.run(main())

from langchain_core.runnables import RunnablePassthrough, RunnableLambda

from apps.entities.chat_models.chat_models import groq_chat
from apps.entities.chains.general_chat_chain.prompt import general_prompt
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
import asyncio


class Answer(BaseModel):
    output: str = Field(description="질문에 대한 답변")


output_parser = JsonOutputParser(pydantic_object=Answer)

prompt = general_prompt.partial(
    format_instructions=output_parser.get_format_instructions()
)

general_chain = prompt | groq_chat | output_parser

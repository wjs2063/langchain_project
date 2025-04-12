from pydantic import BaseModel
from langchain_core.messages import AIMessage


class ChainResponse(BaseModel):
    input: dict
    output: AIMessage

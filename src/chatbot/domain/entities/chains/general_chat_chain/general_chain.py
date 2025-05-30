from chatbot.domain.entities.chat_models.chat_models import groq_chat
from chatbot.domain.entities.chains.general_chat_chain.prompt import general_prompt
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field


class Answer(BaseModel):
    """
    Represents an answer model used to encapsulate a response to a question.

    This class is a data model structured to store and represent the response
    or answer provided for a specific question. It utilizes Pydantic's BaseModel
    to ensure proper validation and structure of data provided during
    initialization. The `output` attribute holds the textual answer. This class
    can be extended or utilized in various application scenarios requiring
    standardized response data representation.

    Attributes:
        output (str): The response or answer related to a given question. Specific
            description provided to clarify its usage.
    """

    output: str = Field(description="질문에 대한 답변")


output_parser = JsonOutputParser(pydantic_object=Answer)

prompt = general_prompt.partial(
    format_instructions=output_parser.get_format_instructions()
)

general_chain = prompt | groq_chat | output_parser

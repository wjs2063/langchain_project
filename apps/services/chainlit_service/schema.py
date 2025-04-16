from pydantic import BaseModel, model_validator, field_validator
from langchain_core.messages import AIMessage


class ChainResponse(BaseModel):
    """
    Represents a chain response model for AI message generation.

    This class is used to handle inputs in dictionary format and process them
    to produce an AI-generated message as the output. It leverages BaseModel
    for validation and other utility features.

    Attributes:
        input (dict): The input data for processing, structured as a dictionary.
        output (AIMessage): The result of the processing, represented as an
            AI message format.
    """

    input: dict
    output: AIMessage

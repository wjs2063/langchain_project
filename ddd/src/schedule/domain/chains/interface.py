from abc import ABC, abstractmethod
from langchain_core.runnables import RunnableSequence
from langchain_core.messages import AIMessage


class AbstractProcessingChain(ABC):
    """
    Abstract base class for creating processing chains with operations that
    validate data, process chains, and parse responses. Subclasses must implement
    abstract methods to provide specific functionality.
    """

    def __init__(self, client_information: dict):
        self.client_information = client_information
        self.chain: RunnableSequence | None = None

    @classmethod
    def parse_response(cls, response) -> str:
        """Parses various types of responses into a string."""
        response_mapping = {
            str: lambda r: r,
            AIMessage: lambda r: r.content,
            dict: lambda r: r.get("output"),
        }
        response_type = type(response)
        if response_type in response_mapping:
            return response_mapping[response_type](response)
        raise ValueError(f"Invalid response type: {response_type}")

    @staticmethod
    @abstractmethod
    def meets_condition(input_data: dict) -> bool:
        """Checks if the processing chain applies to the given input data."""
        raise NotImplementedError

    @abstractmethod
    async def arun(self, request_information: dict) -> dict:
        """Asynchronously processes the request and returns a response."""
        raise NotImplementedError

    @abstractmethod
    def run(self) -> AIMessage:
        """Synchronously processes the request and returns an AIMessage."""
        raise NotImplementedError

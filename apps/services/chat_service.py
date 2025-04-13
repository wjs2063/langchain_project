from abc import ABC, abstractmethod

from langchain_core.runnables import RunnableSequence

from apps.services.schema import ChainResponse
from apps.entities.chains.weather_chain.weather_chain import weather_agent
from apps.entities.chains.schedule_chain.chain import schedule_agent
from apps.entities.chains.general_chat_chain.general_chain import general_chain
from langchain.chains.base import Chain
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from apps.entities.chains.wikipedia_chain.wikipedia_chain import wikipedia_chain


class AbstractProcessingChain(ABC):
    """
    AbstractProcessingChain serves as a blueprint for creating processing chains
    based on specific client information. It defines the structure and required
    methods to be implemented by subclasses, ensuring compatibility and extending functionality.

    This abstract base class is designed to work with processing chains that execute specific
    operations asynchronously or synchronously, validate input data based on conditions, and
    parse various types of responses. Subclasses must override the abstract methods to provide
    their own implementation details.

    Attributes:
        client_information (dict): A dictionary containing client-specific details that influence
        the behavior of the processing chain.
        chain (RunnableSequence): Represents the processing chain. Must be initialized later
        in subclasses.
    """

    def __init__(self, client_information: dict):
        self.client_information = client_information
        self.chain: RunnableSequence | None = None

    @classmethod
    def parse_response(cls, response):
        if isinstance(response, str):
            output = response
        elif isinstance(response, AIMessage):
            output = response.content
        elif isinstance(response, dict):
            output = response["output"]
        else:
            raise ValueError("Invalid response")
        return output

    @staticmethod
    @abstractmethod
    def meets_condition(data: dict) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def arun(self, request_information) -> dict:
        raise NotImplementedError

    @abstractmethod
    def run(self) -> AIMessage:
        raise NotImplementedError


class WeatherChain(AbstractProcessingChain):
    """
    A class representing a processing chain for weather-related queries.

    This class extends the AbstractProcessingChain and is intended to handle queries
    related to weather information. It processes input data and interacts with
    a weather agent to retrieve and deliver weather-related responses. The chain
    ensures that it operates under the correct domain ("weather") and provides
    asynchronous functionality to handle real-time or asynchronous data processing.
    """

    def __init__(self, client_information: dict, weather_chain=weather_agent):
        super().__init__(client_information)
        self.chain = weather_chain

    @staticmethod
    def meets_condition(data) -> bool:
        return data["domain"] == "weather"

    async def arun(self, request_information: dict) -> ChainResponse:
        """
        weather chain's input requirements
        question : str
        """
        request_information = request_information.copy()
        response = await self.chain.ainvoke(
            {
                "question": request_information["question"],
                "chat_history": request_information["chat_history"],
                "user_info": request_information["user_info"],
            }
        )
        output = WeatherChain.parse_response(response)
        # TODO : Call weather chain
        return ChainResponse(
            input=request_information, output=AIMessage(content=output)
        )

    def run(self) -> AIMessage:
        return AIMessage()


class ScheduleChain(AbstractProcessingChain):
    """
    Represents a processing chain specifically used for scheduling-related tasks.

    The ScheduleChain is an extension of the AbstractProcessingChain and is
    used to manage and execute operations associated with the "schedule"
    domain. It contains functionality to determine its applicability based on
    input data and processes requests using an underlying chain dedicated to
    scheduling.

    Attributes:
        chain: The processing chain responsible for handling scheduling tasks.

    """

    def __init__(
        self,
        client_information: dict,
        schedule_chain=schedule_agent,
    ):
        super().__init__(client_information)
        self.chain = schedule_chain

    @staticmethod
    def meets_condition(data: dict) -> bool:
        return data["domain"] == "schedule"

    async def arun(self, request_information: dict) -> ChainResponse:
        request_information = request_information.copy()
        response = await self.chain.ainvoke(
            {
                "question": request_information["question"],
                "chat_history": request_information["chat_history"],
                "user_info": request_information["user_info"],
            }
        )
        output = ScheduleChain.parse_response(response)
        return ChainResponse(
            input=request_information, output=AIMessage(content=output)
        )

    def run(self) -> AIMessage:
        return AIMessage()


class GeneralChain(AbstractProcessingChain):
    """
    Represents a specialized processing chain for handling general queries.

    The GeneralChain class inherits from AbstractProcessingChain and serves as
    a specific implementation for processing data pertaining to the 'general'
    domain. It provides methods to invoke a predefined chain asynchronously or
    synchronously, ensuring that the provided data meets specified conditions
    and formatting the output accordingly.

    Attributes:
    chain : general_chain
        The processing chain that handles specific requests.

    Methods:
    __init__(client_information: dict, general_chain)
        Initializes the GeneralChain instance with client information and the
        processing chain.

    meets_condition(data: dict) -> bool
        Static method that checks if the provided data matches the 'general'
        domain condition.

    arun(request_information: dict) -> ChainResponse
        Asynchronously processes the input request information and invokes the
        associated chain asynchronously. Returns a ChainResponse object.

    run() -> AIMessage
        Synchronously invokes the chain and returns the processed AI message.
    """

    def __init__(
        self,
        client_information: dict,
        general_chain=general_chain,
    ):
        super().__init__(client_information)
        self.chain = general_chain

    @staticmethod
    def meets_condition(data: dict) -> bool:
        return data["domain"] == "general"

    async def arun(self, request_information: dict) -> ChainResponse:
        request_information = request_information.copy()
        response = await self.chain.ainvoke(
            {
                "question": request_information["question"],
                "chat_history": request_information["chat_history"],
                "user_info": request_information["user_info"],
            }
        )
        output = GeneralChain.parse_response(response)
        return ChainResponse(
            input=request_information, output=AIMessage(content=output)
        )

    def run(self) -> AIMessage:
        return AIMessage()


class WikipediaChain(AbstractProcessingChain):
    """
    Chain handling interactions specific to Wikipedia.

    The WikipediaChain class processes input data related to Wikipedia queries and
    uses an underlying chain to process questions and retrieve relevant responses
    based on the provided context such as chat history and user information.
    """

    def __init__(self, client_information: dict):
        super().__init__(client_information)
        self.chain = wikipedia_chain

    @staticmethod
    def meets_condition(data: dict) -> bool:
        return data["domain"] == "wikipedia"

    async def arun(self, request_information: dict) -> ChainResponse:
        request_information = request_information.copy()
        response = await self.chain.ainvoke(
            {
                "question": request_information["question"],
                "chat_history": request_information["chat_history"],
                "user_info": request_information["user_info"],
            }
        )
        output = WikipediaChain.parse_response(response)
        return ChainResponse(
            input=request_information, output=AIMessage(content=output)
        )

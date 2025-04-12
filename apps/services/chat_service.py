from abc import ABC, abstractmethod

from langchain_core.runnables import RunnableSequence

from apps.services.schema import ChainResponse
from apps.entities.chains.weather_chain.weather_chain import weather_agent
from apps.entities.chains.schedule_chain.chain import schedule_agent
from apps.entities.chains.general_chat_chain.general_chain import general_chain
from langchain.chains.base import Chain
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from apps.entities.chains.wikipedia_chain.wikipedia_chain import wikipedia_chain


class BaseChain(ABC):
    """
    Represents an abstract base chain for processing client requests.

    This class serves as a base for creating chains that handle client
    information and execute specific operations depending on the
    implemented methods. It provides a framework for defining chains
    with an abstract structure that subclasses must implement.

    Attributes:
        client_information (dict): A dictionary containing information
            related to the client.
        chain (RunnableSequence): A sequence to be executed as part of
            the chain's workflow.

    Methods:
        parse_response(response):
            Parses and extracts the output from a given response of
            varying types including string, AIMessage, or dictionary.

        meets_condition(data):
            Checks if the provided data satisfies specific conditions.
            Subclasses must implement this method.

        arun(request_information):
            Asynchronously processes a request with the given information
            and returns a dictionary response. Subclasses must implement
            this method.

        run():
            Synchronously executes the chain's process and returns an
            AIMessage. Subclasses must implement this method.
    """

    def __init__(self, client_information: dict):
        self.client_information = client_information
        self.chain: RunnableSequence

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


class WeatherChain(BaseChain):
    """
    WeatherChain is a specialized implementation of the BaseChain tailored for
    processing weather-related queries. It leverages a weather-specific
    processing agent to fulfill and respond to user requests within the
    context of weather data and conversations.

    This class is responsible for determining the relevance of the input data
    to weather-related queries, invoking a weather agent to process input
    asynchronously, and returning structured responses. It operates as a
    chained component suitable for integration into larger systems handling
    domain-specific user interactions.
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


class ScheduleChain(BaseChain):
    """
    Represents a schedule chain process within a chain system.

    The class provides methods to check applicable conditions and facilitate asynchronous
    or synchronous interaction with a schedule agent chain. It encapsulates the logic for
    handling input request information and generating the corresponding responses using
    an agent-based approach.

    Attributes:
        chain: The schedule chain agent used to process input request information.

    Methods:
        meets_condition(data): Checks if the input data meets specific criteria for
            the schedule domain.
        arun(request_information): Asynchronously processes the given request
            information and returns a ChainResponse object.
        run(): Synchronously generates an AIMessage instance.
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


class GeneralChain(BaseChain):
    """
    Represents a general-purpose chain for processing data in a defined format.

    This class extends the BaseChain and provides an implementation for handling
    general-type data. It uses an injected general chain for managing specific
    operational details and includes methods for verifying conditions and
    processing requests asynchronously.
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


class WikipediaChain(BaseChain):
    """
    A chain implementation for handling Wikipedia-specific queries.

    The WikipediaChain class is designed to process queries related to
    Wikipedia by interacting with a predefined chain. It serves as an
    integration point for processing user data and invoking a suitable
    response chain for handling queries within the "wikipedia" domain.

    Attributes:
    chain: The predefined chain handling Wikipedia-related queries.

    Methods:
    - meets_condition(data): Static method to verify if the provided data is
      within the "wikipedia" domain.
    - arun(request_information): Asynchronous method to process the request
      information and invoke the chain to generate a response.
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

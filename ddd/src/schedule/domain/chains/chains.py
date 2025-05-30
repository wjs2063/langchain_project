from abc import ABC, abstractmethod

from langchain_core.runnables import RunnableSequence

from services.chatting_service.schema import ChainResponse
from apps.entities.chains.weather_chain.weather_chain import weather_agent
from apps.entities.chains.schedule_chain.chain import (
    schedule_command_select_chain,
    schedule_response_chain,
)
from apps.entities.chains.schedule_chain.executors import AbstractCommandExecutor
from datetime import datetime
from zoneinfo import ZoneInfo
from apps.entities.chains.general_chat_chain.general_chain import general_chain
from langchain_core.messages import AIMessage
from apps.entities.chains.wikipedia_chain.wikipedia_chain import wikipedia_chain
from interface import AbstractProcessingChain


class ScheduleChain(AbstractProcessingChain):
    """
    Represents a processing chain specifically used for scheduling-related tasks.
    """

    SCHEDULE_DOMAIN = "schedule"

    def __init__(self, client_information: dict):
        super().__init__(client_information)
        self.schedule_command_select_chain = schedule_command_select_chain

    @staticmethod
    def meets_condition(input_data: dict) -> bool:
        return input_data["domain"] == ScheduleChain.SCHEDULE_DOMAIN

    # @trace(logger=logger)
    async def arun(self, request_information: dict) -> ChainResponse:
        # Create a copy to ensure original data isn't modified
        request_information = request_information.copy()

        # Extract and pass the current date-time as a variable for clarity
        current_datetime = datetime.now(ZoneInfo("Asia/Seoul")).isoformat()

        # Invoke schedule command select chain
        command_response = await self.schedule_command_select_chain.ainvoke(
            {
                "chat_history": request_information["chat_history"],
                "question": request_information["question"],
                "current_datetime": current_datetime,
            }
        )

        # Find the matching command executor and execute it
        command_result = await self.find_and_execute_command(command_response)

        # Prepare final response by invoking the scheduling response chain
        final_response = await schedule_response_chain.ainvoke(
            {
                "command_result": command_result,
                "command_type": command_response,
                "question": request_information["question"],
            }
        )

        # Parse and return the final output as a ChainResponse
        parsed_output = ScheduleChain.parse_response(final_response)
        return ChainResponse(
            input=request_information, output=AIMessage(content=parsed_output)
        )

    # @trace(logger=logger)
    async def find_and_execute_command(self, command_response: dict) -> dict:
        """
        Finds and executes the matching command executor for the given response.
        """
        for CommandExecutor in AbstractCommandExecutor.__subclasses__():
            if CommandExecutor.meets_condition(command_response):
                return await CommandExecutor(
                    schedule_command_response=command_response
                ).aexecute()
        raise ValueError("No matching CommandExecutor found.")

    def run(self):
        pass


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

    GENERAL_DOMAIN = "general"

    def __init__(
        self,
        client_information: dict,
        general_chain=general_chain,
    ):
        super().__init__(client_information)
        self.chain = general_chain

    @staticmethod
    def meets_condition(input_data: dict) -> bool:
        return input_data["domain"] == GeneralChain.GENERAL_DOMAIN

    # @trace(logger=logger)
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

    WIKIPEDIA_DOMAIN = "wikipedia"

    def __init__(self, client_information: dict):
        super().__init__(client_information)
        self.chain = wikipedia_chain

    @staticmethod
    def meets_condition(input_data: dict) -> bool:
        return input_data["domain"] == WikipediaChain.WIKIPEDIA_DOMAIN

    # @trace(logger=logger)
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

    def run(self):
        pass

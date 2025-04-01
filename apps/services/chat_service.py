from abc import ABC, abstractmethod

from tenacity import stop_after_attempt

from apps.entities.chains.weather_chain.weather_chain import weather_agent
from apps.entities.chains.schedule_chain.chain import schedule_agent
from apps.entities.chains.general_chat_chain.general_chain import general_chain
from langchain.chains.base import Chain
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from apps.entities.chains.wikipedia_chain.wikipedia_chain import wikipedia_chain


class BaseChain(ABC):

    def __init__(self, client_information: dict):
        self.client_information = client_information
        self.chain = None

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

    def __init__(self, client_information: dict, weather_chain=weather_agent):
        super().__init__(client_information)
        self.chain = weather_chain

    @staticmethod
    def meets_condition(data) -> bool:
        return data["domain"] == "weather"

    async def arun(self, request_information: dict) -> dict:
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
        return {"input": request_information, "output": AIMessage(content=output)}

    def run(self) -> AIMessage:
        return AIMessage()


class ScheduleChain(BaseChain):
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

    async def arun(self, request_information: dict) -> dict:
        # TODO : call schedule_chain
        request_information = request_information.copy()
        response = await self.chain.ainvoke(
            {
                "question": request_information["question"],
                "chat_history": request_information["chat_history"],
                "user_info": request_information["user_info"],
            }
        )
        output = ScheduleChain.parse_response(response)
        return {"input": request_information, "output": AIMessage(content=output)}

    def run(self) -> AIMessage:
        return AIMessage()


class GeneralChain(BaseChain):
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

    async def arun(self, request_information: dict) -> dict:
        # TODO : call general_chain
        request_information = request_information.copy()
        response = await self.chain.ainvoke(
            {
                "question": request_information["question"],
                "chat_history": request_information["chat_history"],
                "user_info": request_information["user_info"],
            }
        )
        output = GeneralChain.parse_response(response)
        return {"input": request_information, "output": AIMessage(content=output)}

    def run(self) -> AIMessage:
        return AIMessage()


class WikipediaChain(BaseChain):
    def __init__(self, client_information: dict):
        super().__init__(client_information)
        self.chain = wikipedia_chain

    @staticmethod
    def meets_condition(data: dict) -> bool:
        return data["domain"] == "wikipedia"

    async def arun(self, request_information: dict) -> dict:
        request_information = request_information.copy()
        response = await self.chain.ainvoke(
            {
                "question": request_information["question"],
                "chat_history": request_information["chat_history"],
                "user_info": request_information["user_info"],
            }
        )
        output = WikipediaChain.parse_response(response)
        return {"input": request_information, "output": AIMessage(content=output)}

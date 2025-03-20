from abc import ABC, abstractmethod

from tenacity import stop_after_attempt

from apps.entities.chains.weather_chain.weather_chain import weather_agent
from apps.entities.chains.schedule_chain.chain import schedule_agent
from apps.entities.chains.general_chat_chain.general_chain import general_chain
from langchain.chains.base import Chain
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage


class AbstractChain(ABC):

    def __init__(self, client_information: dict, previous_step: dict):
        self.client_information = client_information
        self.previous_step = previous_step

    @staticmethod
    @abstractmethod
    def meets_condition(data: dict) -> bool:
        raise NotImplementedError

    async def arun(self, request_information) -> dict:
        raise NotImplementedError

    def run(self) -> AIMessage:
        raise NotImplementedError


class WeatherChain(AbstractChain):

    def __init__(
        self, client_information: dict, previous_step: dict, weather_chain=weather_agent
    ):
        super().__init__(client_information, previous_step)
        self.chain = weather_chain

    @staticmethod
    def meets_condition(data) -> bool:
        return data["domain"] == "weather"

    @classmethod
    def parse_output(cls, response):
        if isinstance(response, str):
            output = response
        elif isinstance(response, AIMessage):
            output = response.content
        elif isinstance(response, dict):
            output = response["output"]
        return output

    async def arun(self, request_information: dict) -> dict:
        """
        weather chain's input requirements
        question : str
        """
        request_information = request_information.copy()
        response = await self.chain.ainvoke(
            {"question": request_information["question"]}
        )
        output = WeatherChain.parse_output(response)
        # TODO : Call weather chain
        return {"input": request_information, "output": AIMessage(content=output)}

    def run(self) -> AIMessage:
        return AIMessage()


class ScheduleChain(AbstractChain):
    def __init__(
        self,
        client_information: dict,
        previous_step: dict,
        schedule_chain=schedule_agent,
    ):
        super().__init__(client_information, previous_step)
        self.chain = schedule_chain

    @staticmethod
    def meets_condition(data: dict) -> bool:
        return data["domain"] == "schedule"

    @classmethod
    def parse_output(cls, response):
        if isinstance(response, str):
            output = response
        elif isinstance(response, AIMessage):
            output = response.content
        elif isinstance(response, dict):
            output = response["output"]
        return output

    async def arun(self, request_information: dict) -> dict:
        # TODO : call schedule_chain
        request_information = request_information.copy()
        response = await self.chain.ainvoke(
            {
                "question": request_information["question"],
                "chat_history": request_information["chat_history"],
            }
        )
        output = ScheduleChain.parse_output(response)
        return {"input": request_information, "output": AIMessage(content=output)}

    def run(self) -> AIMessage:
        return AIMessage()


class GeneralChain(AbstractChain):
    def __init__(
        self,
        client_information: dict,
        previous_step: dict,
        general_chain=general_chain,
    ):
        super().__init__(client_information, previous_step)
        self.chain = general_chain

    @staticmethod
    def meets_condition(data: dict) -> bool:
        return data["domain"] == "general"

    @classmethod
    def parse_output(cls, response):
        if isinstance(response, str):
            output = response
        elif isinstance(response, AIMessage):
            output = response.content
        elif isinstance(response, dict):
            output = response["output"]
        return output

    async def arun(self, request_information: dict) -> dict:
        # TODO : call general_chain
        request_information = request_information.copy()
        response = await self.chain.ainvoke(
            {
                "chat_history": request_information["chat_history"],
                "question": request_information["question"],
            }
        )
        output = GeneralChain.parse_output(response)
        return {"input": request_information, "output": AIMessage(content=output)}

    def run(self) -> AIMessage:
        return AIMessage()

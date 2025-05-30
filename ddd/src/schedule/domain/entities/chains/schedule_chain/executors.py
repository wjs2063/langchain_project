import os
from dotenv import load_dotenv
from abc import ABC, abstractmethod
from aiohttp import ClientSession
from apps.infras.exeternal_apis.google.calendar.handler import GoogleCalendarHandler
import asyncio

load_dotenv()


class AbstractCommandExecutor(ABC):

    @staticmethod
    @abstractmethod
    def meets_condition(data: dict) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def aexecute(self, *args, **kwargs) -> dict:
        raise NotImplementedError

    @abstractmethod
    def execute(self, *args, **kwargs) -> dict:
        raise NotImplementedError


class ScheduleReadCommandExecutor(AbstractCommandExecutor):
    def __init__(self, schedule_command_response: dict):
        self.schedule_command_response = schedule_command_response

    @staticmethod
    def meets_condition(data: dict) -> bool:
        return data["read_command"] is not None and data["read_command"]["flag"] is True

    async def aexecute(self, *args, **kwargs) -> dict:
        request_json = self.schedule_command_response["read_command"]
        request_json.pop("flag")
        access_token = await GoogleCalendarHandler.fetch_google_calendar_access_token()
        calendar_id = os.getenv("MY_GOOGLE_CALENDAR_USER_ID")
        url = f"https://www.googleapis.com/calendar/v3/calendars/{calendar_id}/events"

        header = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        }

        async with ClientSession(headers=header) as session:
            async with session.get(url=url, params=request_json) as response:
                response = await response.json()
                return response

    def execute(self, *args, **kwargs) -> dict:
        pass


class ScheduleRegisterCommandExecutor(AbstractCommandExecutor):
    def __init__(self, schedule_command_response: dict):
        self.schedule_command_response = schedule_command_response

    @staticmethod
    def meets_condition(data: dict) -> bool:
        return (
            data["register_command"] is not None
            and data["register_command"]["flag"] is True
        )

    async def aexecute(self, *args, **kwargs) -> dict:

        access_token = await GoogleCalendarHandler.fetch_google_calendar_access_token()
        calendar_id = os.getenv("MY_GOOGLE_CALENDAR_USER_ID")
        url = f"https://www.googleapis.com/calendar/v3/calendars/{calendar_id}/events"

        header = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        }

        request_json = self.schedule_command_response["register_command"]
        request_json.pop("flag")
        async with ClientSession(headers=header) as session:
            async with session.post(url=url, json=request_json) as resp:
                response = await resp.json()
                return response

    def execute(self, *args, **kwargs) -> dict:
        pass


# schedule_command_response = schedule_command_select_chain.invoke(
#     {
#         "chat_history": [],
#         "question": "내일 일정 알려줘",
#         "current_datetime": datetime.now(ZoneInfo("Asia/Seoul")).isoformat(),
#     }
# )
# print(schedule_command_response)
#
# schedule_read_command_executor = ScheduleReadCommandExecutor(
#     schedule_command_response=schedule_command_response
# )
#
# schedule_register_command_executor = ScheduleRegisterCommandExecutor(
#     schedule_command_response=schedule_command_response
# )


# asyncio.run(schedule_read_command_executor.aexecute())
# asyncio.run(schedule_register_command_executor.aexecute())

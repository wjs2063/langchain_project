from apps.entities.chat_models.chat_models import base_chat
from apps.entities.chains.schedule_chain.prompt import schedule_prompt
from apps.entities.chains.schedule_chain.schema import ScheduleCommandModel
from langchain_core.output_parsers import JsonOutputParser
from apps.entities.chains.schedule_chain.prompt import schedule_response_prompt
from apps.infras.exeternal_apis.google.calendar.handler import GoogleCalendarHandler
import os
from dotenv import load_dotenv
from abc import ABC, abstractmethod
from aiohttp import ClientSession

load_dotenv()
# schedule_agent = create_tool_calling_agent(
#     llm=base_chat, tools=[fetch_my_schedule, add_my_schedule], prompt=schedule_prompt
# )
#
# schedule_agent = AgentExecutor(
#     agent=schedule_agent,
#     tools=[fetch_my_schedule, add_my_schedule],
#     verbose=True,
#     max_iterations=6,
#     max_execution_time=8,
#     handle_parsing_errors=True,
#     early_stopping_method="force",
# )
# import pytz
# from datetime import datetime, timezone
#
# time_zone = pytz.timezone("Asia/Seoul")
# current_time = datetime.now(time_zone)

# print(
#     schedule_agent.invoke(
#         {"question": "내일 3시 휴대폰 수리 일정 등록해줘", "user_info": current_time}
#     )
# )


schedule_response_chain = schedule_response_prompt | base_chat

output_parser = JsonOutputParser(pydantic_object=ScheduleCommandModel)


prompt = schedule_prompt.partial(
    format_instructions=output_parser.get_format_instructions()
)

schedule_command_select_chain = prompt | base_chat | output_parser


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
import asyncio

# asyncio.run(schedule_read_command_executor.aexecute())
# asyncio.run(schedule_register_command_executor.aexecute())

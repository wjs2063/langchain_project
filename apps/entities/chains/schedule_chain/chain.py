from langchain.agents import create_tool_calling_agent, AgentExecutor
from apps.entities.chat_models.chat_models import base_chat
from apps.entities.tools.schedules.schedule_tool import (
    fetch_my_schedule,
    add_my_schedule,
)
from apps.entities.chains.schedule_chain.prompt import schedule_prompt

schedule_agent = create_tool_calling_agent(
    llm=base_chat, tools=[fetch_my_schedule, add_my_schedule], prompt=schedule_prompt
)

schedule_agent = AgentExecutor(
    agent=schedule_agent,
    tools=[fetch_my_schedule, add_my_schedule],
    verbose=True,
    max_iterations=6,
    max_execution_time=8,
    handle_parsing_errors=True,
)
import pytz
from datetime import datetime, timezone

time_zone = pytz.timezone("Asia/Seoul")
current_time = datetime.now(time_zone)

# print(
#     schedule_agent.invoke(
#         {"question": "내일 3시 휴대폰 수리 일정 등록해줘", "user_info": current_time}
#     )
# )

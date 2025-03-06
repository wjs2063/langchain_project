from langchain.agents import create_tool_calling_agent, AgentExecutor
from apps.entities.chat_models.chat_models import base_chat
from apps.entities.tools.schedules.schedule_tool import fetch_my_schedule
from apps.entities.chains.schedule_chain.prompt import schedule_prompt

schedule_agent = create_tool_calling_agent(
    llm=base_chat, tools=[fetch_my_schedule], prompt=schedule_prompt
)

schedule_agent = AgentExecutor(
    agent=schedule_agent,
    tools=[fetch_my_schedule],
    verbose=True,
    max_iterations=4,
    max_execution_time=4,
    handle_parsing_errors=True,
)


print(schedule_agent.invoke({"question": "오늘 일정 변경해줘"}))

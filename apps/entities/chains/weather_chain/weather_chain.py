from langchain.agents import create_tool_calling_agent, AgentExecutor
from apps.entities.chat_models.chat_models import base_chat, groq_chat
from apps.entities.tools.weathers.weather_tool import get_weather
from apps.entities.chains.weather_chain.prompt import weather_template, weather_prompt

weather_agent = create_tool_calling_agent(
    llm=groq_chat,
    tools=[get_weather],
    prompt=weather_prompt,
)

weather_agent = AgentExecutor(
    agent=weather_agent,
    tools=[get_weather],
    verbose=True,
    max_iterations=4,
    max_execution_time=4,
    handle_parsing_errors=True,
)


# print(weather_agent.invoke({"question": "내일 천호동 날씨 알려줘"})["output"].strip())

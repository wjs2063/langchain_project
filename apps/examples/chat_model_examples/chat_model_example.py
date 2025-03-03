import warnings

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

warnings.filterwarnings("ignore")

load_dotenv()
llm = ChatOpenAI(model="gpt-4o", temperature=0.5)
# Function to measure execution time


"""
caching example
"""
# def timed_completion(prompt):
#     start_time = time.time()
#     result = llm.invoke(prompt)
#     end_time = time.time()
#     return result, end_time - start_time


# prompt = "Explain the concept of caching in three sentences."
# result1, time1 = timed_completion(prompt)
# print(f"First call (not cached):\nResult: {result1}\nTime: {time1:.2f} seconds\n")
#
# # Second call (should be cached)
# result2, time2 = timed_completion(prompt)
# print(f"Second call (cached):\nResult: {result2}\nTime: {time2:.2f} seconds\n")
#
# print(f"Speed improvement: {time1 / time2:.2f}x faster")
#
# # Clear the cache
# redis_cache.clear()
# print("Cache cleared")


"""
prompt_example
"""

# from prompt import prompt
#
# print(prompt.format(product="아이폰"))
# print(prompt.format(product="갤럭시"))
#
# print()

"""
prompt_with_chat_models
"""

# from langchain.schema import HumanMessage,AIMessage
#
#
# result = llm([HumanMessage(content=prompt.format(product="아이폰"))])
# print(result)


"""
chat_model_example with output_parser
"""
# from langchain.output_parsers import CommaSeparatedListOutputParser
# from langchain.schema import HumanMessage, AIMessage
#
# output_parser = CommaSeparatedListOutputParser()
#
# results = llm(
#     [
#         HumanMessage(content="현대자동차가 개발한 대표적인 제품 3개를 알려주세요"),
#         HumanMessage(content=output_parser.get_format_instructions())
#     ]
# )
#
# output = output_parser.parse(results.content)
#
# for result in results:
#     print(result)


"""
chat_models_example with streaming output
"""

# from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
#
# llm = ChatOpenAI(
#     model="gpt-4o",
#     streaming=True,
#     callbacks=[
#         StreamingStdOutCallbackHandler(),
#     ]
#
# )
#
# llm([
#     HumanMessage(content="트럼프와 비트코인의 관계에 대해서 알려주세요")
# ])

"""
memory chat_model_example 
"""

# from apps.entities.memories.memory import conversation_buffer_memory
#
# memory_message_result = conversation_buffer_memory.load_memory_variables({})
# for _ in range(3):
#     message = input()
#
#     message_history = memory_message_result["history"]
#
#     message_history.append(HumanMessage(content=message))
#
#     result = llm(message_history)
#
#     conversation_buffer_memory.save_context(
#         {
#             "input": message
#         },
#         {"output": result.content}
#     )
#
#     print(result)


"""
RedisChatMessageHistory with session_id
"""

# from langchain.memory import RedisChatMessageHistory
# from apps.entities.caches.caches import _redis_url
# from apps.entities.memories.memory import conversation_buffer_memory
#
#
# ## session_id 만 변경하면 redis 특정id에 대한 기록 가져옴 -> session_id만 유지하면 가능함
# redis_history = RedisChatMessageHistory(session_id=None, url=_redis_url)
# redis_history.session_id = "123"
# conversation_buffer_memory.chat_memory = redis_history
#
# memory_message_result = conversation_buffer_memory.load_memory_variables({})
# # print(memory_message_result)
# for _ in range(3):
#     message = input()
#
#     if message == "quit":
#         break
#
#     message_history = memory_message_result["history"]
#
#     message_history.append(HumanMessage(content=message))
#
#     result = llm(message_history)
#
#     conversation_buffer_memory.save_context(
#         {"input": message}, {"output": result.content}
#     )
#
#     print(result)


"""
chat_model_example with tools(tavily)
"""
from entities.tools.search.tavily.tavily_search import tavily_search_tool
from langchain.agents import AgentType, initialize_agent
from langchain_core.prompts.prompt import PromptTemplate

from apps.entities.tools.utils.etc import current_date_tool
from apps.entities.tools.weathers.weather_tool import get_weather
from apps.entities.tools.wikipedias.wikipedia_tool import wiki_tool
from apps.entities.tools.schedules.schedule_tool import get_my_schedule

chat_model_with_tool = ChatOpenAI(model="gpt-4o", temperature=0.5)

# tools = [tavily_search_tool, current_date_tool, wiki_tool, get_weather]
tools = [get_my_schedule, current_date_tool, wiki_tool]
prompt = PromptTemplate(
    template="""
You are a highly competent scheduling Car Assistant and Schedule VPA Assistant. Your job is to answer the user's questions accurately and concisely in Korean.  

Rules:  
1. Understand the user's question and provide an appropriate response.  
2. Use the available tools whenever necessary to fetch relevant information.  
3. Always base your response on the current time and date.  
   - Current time: {current_time}  
4. Do not include URLs in your response.  
   - If an event contains a URL, exclude it from the response.  
   - Since the user is driving, URLs are not useful and should be omitted.  

Response Format:  
{Date}  
1. 제목: {Event Title}  
   - 위치: {Location (omit if unavailable)}  
   - 시간: {Start Time} ~ {End Time} KST  
   - 설명: {Event Summary (설명없음 if unavailable)}  

{Date}  
2. 제목: {Event Title}  
   - 위치: {Location (omit if unavailable)}  
   - 시간: {Start Time} ~ {End Time} KST  
   - 설명: {Event Summary (설명없음 if unavailable)}  

User Question:  
{question}  

Available Tools:  
- fetch_my_schedule: Retrieves the user's schedule.  
- current_date_tool: Provides the current date and time.  
- wiki_tool: Searches for relevant information.  

Objective:  
- Always respond in Korean, even if the user asks in another language.  
- Sort events by date and present them in a structured format.  
- Arrange events in the following order: Title → Location (if available) → Date & Time.  
- Do not include any URLs, links, or clickable elements in the response.  
- Keep the response concise and clear for easy understanding.  

Important:  
- Always respond in Korean.  
- If external information is needed, use the tools before answering.  
- Do not include URLs in the response.  
- If there are no events for the requested date, respond with:  
  "요청하신 날짜에 일정이 없습니다."  

    """,
    input_variables=["question", "current_time"],
)
agent_with_tools = initialize_agent(
    llm=chat_model_with_tool,
    tools=tools,
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    max_iterations=3,
    handle_parsing_errors=True,
    prompt=prompt,
    # kwargs={"input_keys": ["question", "context"]},
)
from langchain.agents import AgentExecutor
import pytz
from datetime import datetime

time_zone = pytz.timezone("Asia/Seoul")
current_time = datetime.now(time_zone)
# print(
#     agent_with_tools.invoke(
#         {"input": {"question": "3일전 일정 알려줘", "current_time": current_time}}
#     )
# )

# llm_with_tools = llm.bind_tools(tools=tools)
# print(llm_with_tools.invoke("내 스케쥴 알려줘"))
# print(agent_with_tools.invoke({"question": "내 스케쥴 알려줘"}))

# chain_with_history = RunnableWithMessageHistory(
#     chainlit_prompt | agent_with_tools,
#     verbose=True,
#     get_session_history=get_history,
#     history_messages_key="chat_history",
#     input_messages_key="question",
# )

# input_key 일치 시켜야함
# agent_with_tools.input_keys = ["chat_history", "question"]
# print(agent_with_tools.input_keys)

# response = agent_with_tools.invoke(input="서울 날씨 알려줘")
# print(response)

"""
Runnable Parallel Example
"""

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel, RunnableWithMessageHistory

_parallel_chat_model_example = ChatOpenAI(model="gpt-4o", temperature=0.5)

joke_chain = (
    ChatPromptTemplate.from_template("tell me a joke about {topic}")
    | _parallel_chat_model_example
)

write_chain = (
    ChatPromptTemplate.from_template("write a 2-line poem about {topic}")
    | _parallel_chat_model_example
)

runnable = RunnableParallel(joke=joke_chain, write=write_chain)

# print(runnable.invoke({"topic": "snow"}))

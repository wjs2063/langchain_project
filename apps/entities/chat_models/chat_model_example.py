import warnings
from langchain_openai import ChatOpenAI
from langchain_core.runnables import ConfigurableField
from langchain.chat_models import init_chat_model
from langchain.schema import HumanMessage, AIMessage
import os
from dotenv import load_dotenv

warnings.filterwarnings("ignore")

load_dotenv()
llm = ChatOpenAI(model="gpt-4o", temperature=0)
# Function to measure execution time
import time
from apps.entities.caches.caches import redis_cache

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

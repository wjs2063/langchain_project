import os

from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import (
    RunnableLambda,
    RunnableParallel,
    RunnablePassthrough,
    RunnableWithFallbacks,
)
from langchain_openai import ChatOpenAI

from apps.entities.tools.geo.geo_info import fetch_coordination_tool

load_dotenv()

llm = ChatOpenAI(model="gpt-4o", temperature=0.5, verbose=True)

example_runnable = RunnablePassthrough() | RunnableParallel(
    result=lambda x: llm.invoke("how are you")
)
# print(example_runnable.invoke({"msg": "hello"}))

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "Return User question"),
        ("user", "{question}"),
        # MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)


def get_query(info):
    print("get_query 함수 ", info)
    # if info["input"] == "3":
    #     return {"text": 5}

    return {"text": 7, **info}


def _print_input(info):
    print("_print_input 실행 ", info)
    return info


# 사용자 정의함수의 parameter 는 이전 단계의 output이다
agent = (
    RunnablePassthrough()
    # | RunnableLambda(_print_input)
    | RunnablePassthrough.assign(text=lambda x: x["question"])
    | RunnableLambda(get_query)
    | prompt
    | llm.bind_tools([fetch_coordination_tool])
)

# print(agent.invoke({"input": "5"}))
runnable = (
    RunnablePassthrough()
    | RunnablePassthrough.assign(figure=lambda x: x["msg"] + " assigning success")
    | RunnableLambda(_print_input)
    | RunnablePassthrough.assign(agent_output=lambda x: agent.invoke(x))
    #   # 여기 에서 들어가는 input을
    | RunnableParallel(
        input=RunnablePassthrough(),
        one_result=lambda x: llm.invoke(x["question"]),
        two_result=lambda x: llm.invoke(x["question"]),
    )
    | RunnableLambda(
        lambda x: {
            **x["input"],
            "one_result": x["one_result"],
            "two_result": x["two_result"],
        }
    )
    | RunnableLambda(_print_input)
    | RunnablePassthrough.assign(
        question=lambda x: x["msg"],
    )
    | RunnablePassthrough.assign(agent_result=lambda x: agent.invoke(x))
)


def get_dictionary(input_dict: dict):
    input_dict["three_result"] = input_dict.get("one_result")
    input_dict["four_result"] = input_dict.get("two_result")
    return input_dict


# print(runnable.invoke({"question": "hello", "msg": "hi"}))


runnable = {"topic": RunnablePassthrough()} | RunnablePassthrough()

# print(
#     runnable.invoke({"input": "hello"})
# )  # invoke 로 들어오는 인자가 runnable 의 RunnablePassthrough()로 들어감

runnable = RunnablePassthrough() | RunnablePassthrough()

# print(runnable.invoke("hello"))
from langchain_core.output_parsers import StrOutputParser

chain1 = prompt | llm | StrOutputParser()
chain2 = prompt | llm | StrOutputParser()


def _print(info):
    print("info : ", info)
    return info


runnable = (
    RunnablePassthrough()
    | {"question": chain1}
    | {"output": chain2}
    | RunnableLambda(_print)
)

print(runnable.invoke({"question": "what's the weather today"}))

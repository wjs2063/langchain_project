import os

from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import (RunnableLambda, RunnableParallel,
                                      RunnablePassthrough,
                                      RunnableWithFallbacks)
from langchain_openai import ChatOpenAI

from apps.entities.tools.geo.geo_info import fetch_coordination_tool

load_dotenv()

llm = ChatOpenAI(model="gpt-4o", temperature=0.5, verbose=True)
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "Return User question"),
        ("user", "text"),
        # MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)


def get_query(info):
    print(info)
    if info["input"] == "3":
        return {"text": 5}

    return {"text": 7}


# 사용자 정의함수의 parameter 는 이전 단계의 output이다
agent = (
    RunnablePassthrough()
    | RunnablePassthrough.assign(text=lambda x: x["input"] * 3)
    | RunnableLambda(get_query)
    | prompt
    | llm.bind_tools([fetch_coordination_tool])
)

print(agent.invoke({"input": "5"}))

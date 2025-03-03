import chainlit as cl
from apps.infras.redis._redis import _redis_url

from langchain.callbacks.tracers import ConsoleCallbackHandler
from apps.entities.memories.history import (
    SlidingWindowBufferRedisChatMessageHistory,
)
from langchain_core.runnables import RunnableWithMessageHistory
from apps.entities.auth.model import User, User_Pydantic
from apps.entities.auth.crypt_passwd import pwd_context
from apps.entities.auth.schema import UserSchema
from apps.entities.chat_models.chat_models import base_chat
from langchain_core.messages import trim_messages
from apps.services.chainlit_service.prompt import chainlit_prompt
from chainlit.message import Message
from langchain.schema import HumanMessage, AIMessage
from datetime import datetime
from apps.entities.chat_models.chat_model_example import agent_with_tools


def get_history(session_id: str):
    return SlidingWindowBufferRedisChatMessageHistory(
        session_id=session_id, url=_redis_url, buffer_size=8
    )


async def get_user(user_id: str, password: str):
    res = await User.filter(user_id=user_id).first()
    if not res:
        raise ValueError(f"회원가입을 진행해주세요")
    if not pwd_context.verify(password, res.password):
        raise ValueError("id와 password 를 확인해주세요")
    return UserSchema(**(await User_Pydantic.from_tortoise_orm(res)).dict())


def get_current_time(*args, **kwargs) -> str:
    _now = datetime.now()
    return f"""
    현재 날짜 : {_now.year}년 {_now.month}월 {_now.day}일 {_now.hour}시 {_now.minute}분 
    """


@cl.password_auth_callback
async def auth_callback(user_id: str, password: str):
    res = await get_user(user_id, password)
    cl.user_session.set(res.user_id, res.user_name)
    return cl.User(
        identifier="admin", metadata={"role": "admin", "provider": "credentials"}
    )


@cl.on_chat_start
async def main():
    user_session_id = "jaehyeon"
    if not user_session_id:
        await cl.Message(content="로그인 정보가 없습니다. 다시 로그인해주세요.").send()
        return
    await cl.Message(
        content=f"안녕하세요! {user_session_id}님! 무엇을 도와드릴까요?!",
    ).send()

    history = SlidingWindowBufferRedisChatMessageHistory(
        session_id=user_session_id, url=_redis_url, buffer_size=8
    )

    chain = chainlit_prompt | agent_with_tools
    chain_with_history = RunnableWithMessageHistory(
        chain,
        verbose=True,
        get_session_history=get_history,
        history_messages_key="history",  # history 의 key값
        input_messages_key="question",  # input_message의 key값
    )
    buffered_history = trim_messages(
        messages=await history.aget_messages(),
        strategy="last",
        start_on="human",
        allow_partial=False,
        max_tokens=100,
        token_counter=len,
    )
    await cl.Message("-" * 10 + "대화 이력" + "-" * 10).send()
    for message in buffered_history:
        if isinstance(message, HumanMessage):
            await cl.Message(author="User", content=f"User : {message.content}").send()
        else:
            await cl.Message(author="VPA", content=f"VPA : {message.content}").send()
    await cl.Message("-" * 20).send()
    cl.user_session.set("chain", chain_with_history)


@cl.on_message
async def on_message(message: Message):
    chain = cl.user_session.get("chain")
    _now = datetime.now()
    user_info = f"""
    현재 날짜 : {_now.year}년 {_now.month}월 {_now.day}일 {_now.hour}시 {_now.minute}분 
    """
    result = await chain.ainvoke(
        {"question": message.content, "ability": "chatting", "user_info": user_info},
        config={
            "configurable": {"session_id": "jaehyeon", "user_id": "jaehyeon"},
            "callbacks": [ConsoleCallbackHandler()],
        },
    )
    await cl.Message(content=result["output"]).send()

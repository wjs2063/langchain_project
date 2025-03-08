from datetime import datetime

import chainlit as cl
from chainlit.message import Message
from langchain.callbacks.tracers import ConsoleCallbackHandler
from langchain.schema import HumanMessage
from langchain_core.messages import trim_messages
from langchain_core.runnables import RunnableWithMessageHistory

from apps.entities.auth.crypt_passwd import pwd_context
from infras.repository.user_repository.model import User, User_Pydantic
from infras.repository.user_repository.schema import UserSchema
from examples.chat_model_examples.chat_model_example import agent_with_tools
from apps.entities.memories.history import SlidingWindowBufferRedisChatMessageHistory
from apps.infras.redis._redis import _redis_url
from apps.services.chainlit_service.prompt import chainlit_prompt
from infras.repository.user_repository.user_repository import (
    AbstractUserRepository,
    UserRepository,
)
from apps.entities.chat_models.chat_models import (
    base_chat,
    ChatOpenAI,
    groq_chat,
    groq_deepseek,
)


class ChatService:
    def __init__(
        self,
        user_repository: AbstractUserRepository,
        chat_model: ChatOpenAI,
        history: SlidingWindowBufferRedisChatMessageHistory,
        session_id: str,
    ):
        self._user_repository = user_repository
        self.chat_model = chat_model
        self.history = history
        self.session_id = session_id

    @staticmethod
    def get_history(session_id: str) -> SlidingWindowBufferRedisChatMessageHistory:
        return SlidingWindowBufferRedisChatMessageHistory(
            session_id=session_id, url=_redis_url, buffer_size=8
        )

    async def display_chat_history(self, cl):
        """
        대화 이력을 화면에 출력하는 함수
        """
        messages = trim_messages(
            messages=await self.history.aget_messages(),
            strategy="last",
            start_on="human",
            allow_partial=False,
            max_tokens=100,
            token_counter=len,
        )
        if not messages:
            return
        history_msgs = ["-" * 10 + "대화 이력" + "-" * 10]

        for msg in messages:
            author = "User" if isinstance(msg, HumanMessage) else "AI"
            history_msgs.append(f"{author} : {msg.content}")

        history_msgs.append("-" * 20)

        for msg in history_msgs:
            await cl.Message(msg).send()
        await cl.Message("-" * 10 + "대화 이력" + "-" * 10).send()

    async def ainvoke(self, message: Message):
        _now = datetime.now()
        user_info = get_current_time()
        result = await self.chat_model.ainvoke(
            {
                "question": message.content,
                "ability": "chatting",
                "user_info": user_info,
            },
            config={
                "configurable": {
                    "session_id": self.session_id,
                    "user_id": self.session_id,
                },
                "callbacks": [],
            },
        )
        return result


def get_current_time(*args, **kwargs) -> str:
    _now = datetime.now()
    return f"""
    현재 날짜 : {_now.year}년 {_now.month}월 {_now.day}일 {_now.hour}시 {_now.minute}분 
    """


async def get_user(user_id: str, password: str):
    user = await UserRepository().get_user(user_id=user_id)
    if not user:
        raise ValueError(f"회원가입을 진행해주세요")
    if not pwd_context.verify(password, user.password):
        raise ValueError("id와 password 를 확인해주세요")
    return UserSchema(**(await User_Pydantic.from_tortoise_orm(user)).dict())


@cl.password_auth_callback
async def auth_callback(user_id: str, password: str):
    res = await get_user(user_id, password)
    # cl.user_session.set(res.user_id, res.user_name)
    return cl.User(
        identifier=res.user_id,
        metadata={"role": res.user_id, "provider": "credentials"},
    )


@cl.on_chat_start
async def main():
    user_res = await cl.AskUserMessage("가져올 세션id를 입력해주세요").send()
    user_session_id = user_res["output"]

    if not user_session_id:
        await cl.Message(content="로그인 정보가 없습니다. 다시 로그인해주세요.").send()
        return
    history = SlidingWindowBufferRedisChatMessageHistory(
        session_id=user_session_id, url=_redis_url, buffer_size=8
    )

    chain_with_history = RunnableWithMessageHistory(
        chainlit_prompt | groq_deepseek,
        verbose=True,
        get_session_history=ChatService.get_history,
        history_messages_key="history",
        input_messages_key="question",
    )
    chat_service = ChatService(
        user_repository=UserRepository(),
        chat_model=chain_with_history,
        history=history,
        session_id=user_session_id,
    )

    await chat_service.display_chat_history(cl)

    await cl.Message(
        content=f"안녕하세요! {user_session_id}님! 무엇을 도와드릴까요?!",
    ).send()
    cl.user_session.set("chat_service", chat_service)


@cl.on_message
async def on_message(message: Message):
    chat_service = cl.user_session.get("chat_service")
    result = await chat_service.ainvoke(message=message)
    await cl.Message(content=result.content).send()

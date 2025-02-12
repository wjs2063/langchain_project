import chainlit as cl
from apps.infras.redis._redis import _redis_url
from langchain_community.chat_message_histories import RedisChatMessageHistory
from langchain.memory import (
    ConversationBufferWindowMemory,
    ConversationSummaryBufferMemory,
)
from langchain.schema import HumanMessage, AIMessage
from langchain.chains.conversation.base import ConversationChain
from apps.entities.memories.history import (
    SlidingWindowBufferRedisChatMessageHistory,
)
from apps.entities.chat_models.chat_model_example import llm
from apps.entities.auth.model import User, User_Pydantic
from apps.entities.auth.crypt_passwd import pwd_context
from apps.entities.auth.schema import UserSchema
from apps.services.chainlit_service.prompt import chainlit_prompt
from tortoise import run_async
from random import randint


async def get_user(user_id: str, password: str):
    res = await User.filter(user_id=user_id).first()
    if not res:
        raise ValueError(f"회원가입을 진행해주세요")
    if not pwd_context.verify(password, res.password):
        raise ValueError("id와 password 를 확인해주세요")
    return UserSchema(**(await User_Pydantic.from_tortoise_orm(res)).dict())


@cl.password_auth_callback
async def auth_callback(user_id: str, password: str):
    # res = syncify(get_user)(user_id=user_id, password=password)
    # res = anyio.to_thread.run_sync(get_user, user_id, password, abandon_on_cancel=True)
    res = await get_user(user_id, password)
    # session_id
    # cl.user_session.set("user_id", res.user_id)
    # print(res, cl.user_session)

    return cl.User(
        identifier="admin", metadata={"role": "admin", "provider": "credentials"}
    )
    # if (user_id, password) == ("admin", "admin"):
    #     return cl.User(
    #         identifier="admin", metadata={"role": "admin", "provider": "credentials"}


@cl.on_chat_start
async def main():
    user_session_id = "jaehyeon1"
    if not user_session_id:
        await cl.Message(content="로그인 정보가 없습니다. 다시 로그인해주세요.").send()
        return
    await cl.Message(
        content=f"안녕하세요! {user_session_id}님! 무엇을 도와드릴까요?!",
    ).send()

    history = SlidingWindowBufferRedisChatMessageHistory(
        session_id=user_session_id, url=_redis_url, buffer_size=8
    )

    memory = ConversationBufferWindowMemory(
        llm=llm, chat_memory=history, return_messages=True, max_token_limit=50, k=8
    )
    chain = ConversationChain(
        memory=memory, llm=llm, prompt=chainlit_prompt, verbose=True
    )

    memory_message_result = await chain.memory.aload_memory_variables({})

    messages = memory_message_result["history"]
    for message in messages:
        print(message)
        if isinstance(message, HumanMessage):
            await cl.Message(author="User", content=f"{message.content}").send()
        else:
            await cl.Message(author="VPA", content=f"{message.content}").send()
    cl.user_session.set("chain", chain)


from chainlit.message import Message


@cl.on_message
async def on_message(message: Message):
    chain = cl.user_session.get("chain")
    result = await chain.apredict(input=message.content)
    print(result)
    await cl.Message(content=result).send()

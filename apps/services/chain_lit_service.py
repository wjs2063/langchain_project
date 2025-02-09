import chainlit as cl
from apps.infras.redis._redis import _redis_url
from langchain_community.chat_message_histories import RedisChatMessageHistory
from langchain.memory import (
    ConversationBufferWindowMemory,
    ConversationSummaryBufferMemory,
)
from langchain.schema import HumanMessage, AIMessage
from langchain.chains.conversation.base import ConversationChain
from apps.entities.memories.history import SlidingWindowBufferRedisChatMessageHistory
from apps.entities.chat_models.chat_model_example import llm


@cl.on_chat_start
async def main():
    user_session_id = None
    while not user_session_id:
        res = await cl.AskUserMessage(
            content="나는 기억할수있는 채팅봇이야! 너를 알아볼수있도록 비밀 password를 지정해줘!",
            timeout=240,
        ).send()
        if res:
            print(res)
            user_session_id = res["output"].strip()

    # history = RedisChatMessageHistory(
    #     session_id=user_session_id,
    #     url=_redis_url,
    # )
    history = SlidingWindowBufferRedisChatMessageHistory(
        session_id=user_session_id, url=_redis_url, buffer_size=8
    )

    print(len(history.messages))

    memory = ConversationSummaryBufferMemory(
        llm=llm, chat_memory=history, return_messages=True, max_token_limit=50
    )
    chain = ConversationChain(memory=memory, llm=llm)

    memory_message_result = chain.memory.load_memory_variables({})

    messages = memory_message_result["history"]
    for message in messages:
        if isinstance(message, HumanMessage):
            await cl.Message(author="User", content=f"{message.content}").send()
        else:
            await cl.Message(author="VPA", content=f"{message.content}").send()
    cl.user_session.set("chain", chain)


from chainlit.message import Message


@cl.on_message
async def on_message(message: Message):
    chain = cl.user_session.get("chain")
    print(message.content)
    result = chain(message.content)
    await cl.Message(content=result["response"]).send()

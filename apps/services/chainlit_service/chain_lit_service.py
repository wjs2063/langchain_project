from datetime import datetime
import traceback
import chainlit as cl
from chainlit.message import Message
from langchain_core.messages import trim_messages

from apps.entities.auth.crypt_passwd import pwd_context
from entities.chains.domain_selector_chain.domain_selector_chain import (
    merge_multi_domain_output,
)
from apps.entities.utils.time import get_current_time
import asyncio
from apps.exceptions.exception_handler import CustomException
from apps.services.chat_service import BaseChain
from infras.repository.user_repository.model import User, User_Pydantic
from infras.repository.user_repository.schema import UserSchema
from apps.entities.memories.history import SlidingWindowBufferRedisChatMessageHistory
from apps.infras.redis._redis import _redis_url
from infras.repository.user_repository.user_repository import (
    AbstractUserRepository,
    UserRepository,
)
from apps.entities.chains.domain_selector_chain.domain_selector_chain import (
    multi_domain_chain,
)
from langchain_core.messages import AIMessage, HumanMessage
from apps.entities.chat_models.chat_models import (
    ChatOpenAI,
)
from apps.entities.chains.merge_output_chain.merge_output_chain import (
    merge_output_chain,
)

"""
1. 질문 분해 (ex. 날씨도 알려주고, 노래도 틀어줘)
-> 날씨도메인 chain 이 날씨를 알려주고, 노래도메인 chain 이 노래를 틀어줘야함 
2. 각 domain 에 해당하는 chain 이 각 결과를 반환 
3. 최종적으로 output 전달 

# key point 는 각 chat_history를 언제 save 할것인가.. 
"""


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
        self.history_buffers: list = list()

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
        history_msgs = ["-" * 10 + "이전 대화 이력" + "-" * 10]

        for msg in messages:
            author = "User" if isinstance(msg, HumanMessage) else "AI"
            history_msgs.append(f"{author} : {msg.content}")

        history_msgs.append("-" * 20)

        for msg in history_msgs:
            await cl.Message(msg).send()
        await cl.Message("-" * 10 + "이전 대화 이력" + "-" * 10).send()

    async def ainvoke(self, message: Message):
        # 첫 질문을 -> 소규모 질문으로 분할
        history = await self.history.aget_messages()
        request_information = {
            "question": message.content,
            "ability": "chatting",
            "chat_history": history,
            "user_info": get_current_time(region="kr"),
        }
        result = await self.chat_model.ainvoke(request_information)
        result = {**result, **request_information}
        response = await self.process_sub_chains(result)
        merged_output = merge_multi_domain_output(response)

        response = await merge_output_chain.ainvoke(
            {"question": message.content, "domain_answers": merged_output.content}
        )
        self.history_buffers.append(
            HumanMessage(content=message.content, additional_kwargs={"test": "kwargs"})
        )
        self.history_buffers.append(
            AIMessage(content=response.content, additional_kwargs={"test": "kwargs"})
        )
        await self.history.aadd_messages(self.history_buffers)
        return response.content

    async def process_sub_chains(self, result):
        try:
            parallel_tasks = set()

            for data in result.get("questions", []):
                for sub_chain in self.get_sub_chains(data):
                    task = asyncio.create_task(
                        sub_chain(
                            client_information={},
                        ).arun(
                            request_information={
                                **data,
                                "chat_history": result["chat_history"],
                                "user_info": result["user_info"],
                            }
                        )
                    )
                    parallel_tasks.add(task)
        except Exception as e:
            error_trace = traceback.format_exc()
            raise CustomException(
                status_code=500, detail=error_trace, trace=error_trace
            )
        else:
            return await asyncio.gather(*parallel_tasks)

    def get_sub_chains(self, data):
        return [
            sub for sub in BaseChain.__subclasses__() if sub.meets_condition(data=data)
        ]


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

    chat_service = ChatService(
        user_repository=UserRepository(),
        chat_model=multi_domain_chain,
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
    # merge_multi_domain_output(result)
    await cl.Message(content=result).send()

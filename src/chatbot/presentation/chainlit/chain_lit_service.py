from datetime import datetime
import chainlit as cl
from chainlit.message import Message
from chatbot.domain.entities.auth.crypt_passwd import pwd_context
from chatbot.infra.repository.user_repository.model import User_Pydantic
from chatbot.infra.repository.user_repository.schema import UserSchema
from chatbot.domain.entities.memories.history import (
    SlidingWindowBufferRedisChatMessageHistory,
)
from chatbot.infra.redis._redis import _redis_url
from chatbot.infra.repository.user_repository.user_repository import (
    UserRepository,
)
from chatbot.domain.entities.chains.domain_selector_chain.domain_selector_chain import (
    multi_domain_chain,
)
from chatbot.application.use_case.chat import ChatService

"""
1. 질문 분해 (ex. 날씨도 알려주고, 노래도 틀어줘)
-> 날씨도메인 chain 이 날씨를 알려주고, 노래도메인 chain 이 노래를 틀어줘야함 
2. 각 domain 에 해당하는 chain 이 각 결과를 반환 
3. 최종적으로 output 전달 

# key point 는 각 chat_history를 언제 save 할것인가.. 
"""


def get_current_time(*args, **kwargs) -> str:
    """
    Retrieve and format the current date and time as a human-readable string.

    This function uses the current local time to construct a formatted string
    representing the date and time in a specific Korean format.

    Args:
        *args: Additional positional arguments, unused.
        **kwargs: Additional keyword arguments, unused.

    Returns:
        str: Formatted string representing the current date and time.
    """
    _now = datetime.now()
    return f"""
    현재 날짜 : {_now.year}년 {_now.month}월 {_now.day}일 {_now.hour}시 {_now.minute}분 
    """


async def get_user(user_id: str, password: str):
    """
    Fetch a user's details from the database and validate their credentials.

    This asynchronous function retrieves a user's account information
    from the database based on the provided user ID. It then verifies
    whether the stored credentials match the provided password. If the
    user is not found or the password is incorrect, a validation error
    is raised. Upon successful validation, the user's details are
    returned in the form of a schema object.

    Arguments:
        user_id: str
            The unique identifier of the user, which is required for
            fetching their details from the database.
        password: str
            The plaintext password provided by the user. It will be
            compared against the hashed password stored in the
            database for verification.

    Raises:
        ValueError
            Raised if the provided credentials are invalid. Specifically,
            an error occurs if the user does not exist or if the password
            does not match the value stored in the database.

    Returns:
        UserSchema
            An object containing the user's detailed information, formatted
            according to the UserSchema structure, if authentication is
            successful.
    """
    user = await UserRepository().get_user(user_id=user_id)
    if not user:
        raise ValueError(f"회원가입을 진행해주세요")
    if not pwd_context.verify(password, user.password):
        raise ValueError("id와 password 를 확인해주세요")
    return UserSchema(**(await User_Pydantic.from_tortoise_orm(user)).dict())


@cl.password_auth_callback
async def auth_callback(user_id: str, password: str):
    """
    Asynchronous callback function for password-based authentication that verifies user credentials and returns user data.

    Arguments:
        user_id: A string representing the unique identifier of the user.
        password: A string representing the password of the user.

    Returns:
        cl.User: A user object containing the verified user's identifier and
        metadata including their role and authentication provider.
    """
    res = await get_user(user_id, password)
    # cl.user_session.set(res.user_id, res.user_name)
    return cl.User(
        identifier=res.user_id,
        metadata={"role": res.user_id, "provider": "credentials"},
    )


@cl.on_chat_start
async def main():
    """
    Asynchronous function that initiates a chat session, retrieves a session ID
    from the user, and sets up necessary services for chat interaction. It also
    integrates Redis-based history management and sends relevant messages to the user.

    Parameters:
        None

    Raises:
        None

    Returns:
        None
    """
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
    """
    An asynchronous function that handles incoming messages and processes them using a chat service.

    The function retrieves the chat_service object from the user session,
    invokes the chat_service with the received message, and sends the processed
    output as a new chat message.

    Args:
        message (Message): The incoming message object to be processed.

    Returns:
        None
    """
    chat_service = cl.user_session.get("chat_service")
    result = await chat_service.ainvoke(message=message)
    # merge_multi_domain_output(result)
    await cl.Message(content=result).send()

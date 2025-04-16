from fastapi import APIRouter, Depends, Request, Response
from apps.entities.memories.history import SlidingWindowBufferRedisChatMessageHistory
from apps.infras.redis._redis import _redis_url
from infras.repository.user_repository.user_repository import (
    UserRepository,
)
from apps.entities.chains.domain_selector_chain.domain_selector_chain import (
    multi_domain_chain,
)
from apps.services.chatting_service.chatting_service import ChatService
from apps.infras.utils.loggings.decorator import trace
from apps.infras.utils.loggings.root import logger

chat_router = APIRouter()


@chat_router.post("/{user_session_id}")
@trace(logger=logger)
async def chat_handler(
    question: str = "내일 일정 알려줘",
    user_session_id: str = "123",
):

    history = SlidingWindowBufferRedisChatMessageHistory(
        session_id=user_session_id, url=_redis_url, buffer_size=8
    )

    chat_service = ChatService(
        user_repository=UserRepository(),
        chat_model=multi_domain_chain,
        history=history,
        session_id=user_session_id,
    )

    # raise CustomException(
    #     status_code=404, detail="Not Found", trace=traceback.format_exc()
    # )
    return await chat_service.ainvoke(message=question)

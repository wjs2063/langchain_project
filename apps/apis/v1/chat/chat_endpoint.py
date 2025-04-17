from fastapi import APIRouter, Depends, Request, Response

from apis.v1.chat.schema import ClientInformation
from apps.entities.memories.history import SlidingWindowBufferRedisChatMessageHistory
from apps.infras.redis._redis import _redis_url
from infras.repository.user_repository.user_repository import (
    UserRepository,
)
from apps.entities.chains.domain_selector_chain.domain_selector_chain import (
    multi_domain_chain,
)
from apps.services.chatting_service.chatting_service import ChatService
from apps.infras.utils.loggings.usecase import trace
from apps.infras.utils.loggings.root import logger
from apps.core.routers.log_routes.log_routes import LogRoute
from infras.utils.decorators.exceptions.exception_handler import (
    register_exception_handler,
)

chat_router = APIRouter(route_class=LogRoute)


@chat_router.post("/")
@register_exception_handler
async def chat_handler(
    client_information: ClientInformation,
):

    history = SlidingWindowBufferRedisChatMessageHistory(
        session_id=client_information.session_id, url=_redis_url, buffer_size=8
    )
    chat_service = ChatService(
        user_repository=UserRepository(),
        chat_model=multi_domain_chain,
        history=history,
        session_id=client_information.session_id,
    )

    # raise CustomException(
    #     status_code=404, detail="Not Found", trace=traceback.format_exc()
    # )
    return await chat_service.ainvoke(message=client_information.question)

from fastapi import APIRouter

from apis.v1.chat.schema import ClientInformation

chat_router = APIRouter()


@chat_router.post("/")
async def chat_handler(
    client_information: ClientInformation,
):
    pass

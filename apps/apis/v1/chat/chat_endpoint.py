from fastapi import APIRouter, Request, Depends, Response

chat_router = APIRouter()


@chat_router.post("/")
async def chat_handler(request: Request):
    return {"msg": "chat_handler"}

from fastapi import APIRouter, Depends, Request, Response

chat_router = APIRouter()


@chat_router.post("/")
async def chat_handler(request: Request):
    return {"msg": "chat_handler"}

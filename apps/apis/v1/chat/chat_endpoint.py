from fastapi import APIRouter, Depends, Request, Response
from pydantic import BaseModel, model_validator

chat_router = APIRouter()


@chat_router.post("/")
async def chat_handler(request: Request):
    return {"msg": "chat_handler"}

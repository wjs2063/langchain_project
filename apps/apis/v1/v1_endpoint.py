from fastapi import APIRouter, Request
from langchain.chat_models import init_chat_model
import os
from dotenv import load_dotenv
from chainlit.utils import mount_chainlit

load_dotenv()
chat_router = APIRouter()


@chat_router.post("/chat")
async def chat_service(request: Request):
    return

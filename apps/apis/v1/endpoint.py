from fastapi import APIRouter, Request
from langchain.chat_models import init_chat_model
import os
from dotenv import load_dotenv

load_dotenv()
api_router = APIRouter()



@api_router.post("/")
async def chat_service(request: Request):
    return

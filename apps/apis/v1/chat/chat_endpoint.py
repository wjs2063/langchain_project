from fastapi import APIRouter, Depends, Request, Response
from pydantic import BaseModel, model_validator
import traceback
from exceptions.exception_handler import CustomException

chat_router = APIRouter()


@chat_router.post("/")
async def chat_handler(request: Request):
    raise CustomException(
        status_code=404, detail="Not Found", trace=traceback.format_exc()
    )
    return {"msg": "chat_handler"}

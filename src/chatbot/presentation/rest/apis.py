from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException

from chatbot.domain.entities.auth.crud import create_user
from chatbot.domain.entities.auth.crypt_passwd import pwd_context
from chatbot.infra.repository.user_repository.schema import UserCreate, UserSchema
from chatbot.infra.repository.user_repository.user_repository import user_repository

load_dotenv()

chatbot_router = APIRouter()


@chatbot_router.post("/user/singup")
async def sigunp_for_chatbot(user_create: UserCreate):
    try:
        user = UserSchema(
            user_id=user_create.user_id,
            user_name=user_create.user_name,
            password=pwd_context.hash(user_create.password1),
        )
        await create_user(user)
    except Exception as e:
        raise HTTPException(detail=str(e), status_code=500)
    return {"message": "User created successfully"}


@chatbot_router.get("/user")
async def get_user(user_id: str):
    try:
        user = await user_repository.get_user(user_id=user_id)
    except Exception as e:
        raise HTTPException(detail=str(e), status_code=404)
    return user

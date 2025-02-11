from fastapi import APIRouter, Depends, HTTPException
from jose import jwt
from fastapi.security import OAuth2PasswordRequestForm
from dotenv import load_dotenv
from apps.entities.auth.schema import UserCreate, UserSchema
from apps.entities.auth.model import User, User_Pydantic
from apps.entities.auth.crypt_passwd import pwd_context
from apps.entities.auth.crud import create_user

load_dotenv()

auth_router = APIRouter()


@auth_router.post("/user/singup")
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

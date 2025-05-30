from chatbot.infra.repository.user_repository.model import User, User_Pydantic
from chatbot.infra.repository.user_repository.schema import UserSchema


async def create_user(user: UserSchema) -> UserSchema:
    if await User.exists(user_id=user.user_id):
        raise ValueError(f"User {user.user_id} already exists")
    res = await User.create(**user.model_dump())
    return await User_Pydantic.from_tortoise_orm(res)

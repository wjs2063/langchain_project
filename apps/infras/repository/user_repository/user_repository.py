from abc import ABC, abstractmethod
from tortoise.transactions import atomic
from apps.infras.repository.user_repository.model import User, User_Pydantic
from apps.infras.repository.user_repository.schema import UserSchema
from tortoise.exceptions import (
    DoesNotExist,
    ValidationError,
    ObjectDoesNotExistError,
    DBConnectionError,
)


class AbstractUserRepository(ABC):

    @abstractmethod
    async def create_user(self, user: User) -> User:
        raise NotImplementedError

    @abstractmethod
    async def get_user(self, user_id: str) -> User:
        raise NotImplementedError


class UserRepository(AbstractUserRepository):

    @atomic
    async def create_user(self, user: UserSchema) -> User:
        pass

    async def get_user(self, user_id: str) -> User:
        try:
            user = await User.get(user_id=user_id).first()
        except Exception as e:
            raise DoesNotExist(User)
        return user


user_repository = UserRepository()

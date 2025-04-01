from pydantic import BaseModel, EmailStr, field_validator
from pydantic_core.core_schema import FieldValidationInfo


class Token(BaseModel):
    access_token: str
    token_type: str
    username: str


class UserCreate(BaseModel):
    user_id: str
    user_name: str
    password1: str
    password2: str
    email: EmailStr

    @classmethod
    @field_validator("user_id", "user_name", "password1", "password2")
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("빈 값은 허용되지 않습니다.")
        return v

    @classmethod
    @field_validator("password2")
    def passwords_match(cls, v, info: FieldValidationInfo):
        if "password1" in info.data and v != info.data["password1"]:
            raise ValueError("비밀번호가 일치하지 않습니다")
        return v


class UserSchema(BaseModel):
    user_id: str
    user_name: str
    password: str

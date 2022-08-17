from app.schemas.base import BaseModelORM
from pydantic import Field


class BaseUserModel(BaseModelORM):
    login: str = Field(..., title="Login")


class RegisterUserModel(BaseUserModel):
    password: str = Field(..., min_length=6, title="Password")


class UserCreated(BaseModelORM):
    detail: str = Field(default="User created")
    uuid: str

from pydantic import (
    BaseModel,
    EmailStr
)

from typing import Literal


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

    role: Literal[
        "SUPER_ADMIN",
        "ADMIN",
        "DOCTOR"
    ] = "DOCTOR"


class UserLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
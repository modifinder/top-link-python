# -*- coding:utf-8 -*-

from typing import Any, Union, List, Optional
from pydantic import BaseModel, Field


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str


class TokenPayload(BaseModel):
    sub: str = None
    exp: int = None


class UserBase(BaseModel):
    user_name: str
    email: Optional[str]


class UserAuth(UserBase):
    password: str


class UserCreate(UserBase):
    enable: bool
    create_time: int
    update_time: int
    hashed_password: str


class Response(BaseModel):
    code: int = 0
    msg: str = "ok"
    data: Any = None


class ResponseWithCount(Response):
    count: int


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


class StringData(BaseModel):
    data: Union[str, None] = None

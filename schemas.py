# -*- coding:utf-8 -*-

from typing import Any, Union, List, Optional
from pydantic import BaseModel, Field, ValidationError, validator
from utils import is_email


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str


class TokenPayload(BaseModel):
    sub: str = None
    exp: int = None


class UserBase(BaseModel):
    user_name: str
    email: Optional[str]

    @validator('user_name')
    def user_name_must_be_alphanumeric_and_len_between_four_and_sixteen(cls, v):
        # 用户名只能是字母或数字
        if not v.isalnum():
            raise ValueError('must be alphanumeric')
        # 长度检查
        if len(v) <= 4 or len(v) >= 16:
            raise ValueError('must be between 4 and 16 characters')
        return v

    @validator('email')
    def email_must_be_valid(cls, v):
        if not is_email(v):
            raise ValueError('must be a valid email address')
        return v


class UserRegister(UserBase):
    password: str = Field(..., min_length=6, max_length=16)
    interest_primary_code: int
    field_code: int

    @validator('password')
    def password_must_be_len_between_six_and_sixteen(cls, v):
        if len(v) <= 6 or len(v) >= 16:
            raise ValueError('must be between 6 and 16 characters')
        return v


class UserAuth(UserBase):
    password: str


class UserInfo(UserBase):
    user_id: int


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


class UploadImage(BaseModel):
    origin: str
    image_b64: str


class LinkBase(BaseModel):
    lid: str
    thumb: str
    url: str
    title: str
    position: int
    display: bool = True
    type: str = "default"


class LinkCreate(LinkBase):
    user_id: int


class LinkUpdate(BaseModel):
    links: List[LinkBase]


class SettingBase(BaseModel):
    page_title: str
    page_bio: str
    profile_picture: str


class SettingCreate(SettingBase):
    user_id: int
    user_name: str
    theme: str = "default"
    page_title: str = ""
    page_bio: str = ""
    profile_picture: str = "/top/images/avatar/default.jpg"
    interest_primary_code: int = 1
    field_code: int = 1
    verified: int = 0
    auth_content: str = ""
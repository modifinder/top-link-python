# -*- coding:utf-8 -*-

from typing import Any
from pydantic import BaseModel


class Response(BaseModel):
    code: int = 0
    msg: str = "ok"
    data: Any = None


class ResponseWithCount(Response):
    count: int

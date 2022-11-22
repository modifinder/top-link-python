# -*- coding:utf-8 -*-

import time
from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from utils import (
    get_hashed_password,
    create_access_token,
    create_refresh_token,
    verify_password
)

from deps import get_current_user, get_db
import crud
import schemas
import models

router = APIRouter()


@router.get("/{username}")
async def get_user_setting(username: str, db: Session = Depends(get_db)):
    """根据用户名页面设置信息"""
    user = crud.get_user_by_user_name(db, username)
    if not user:
        raise HTTPException(
            status_code=400,
            detail="not found this user"
        )
    user_setting = crud.get_setting_by_user_id(db, user.id)
    return schemas.Response(data=user_setting)

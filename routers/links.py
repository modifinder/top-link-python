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
async def get_links(username: str, db: Session = Depends(get_db)):
    """根据用户名获取链接"""
    user = crud.get_user_by_user_name(db, username)
    if not user:
        raise HTTPException(
            status_code=400,
            detail="not found this user"
        )
    links = crud.get_links_by_user_id(db, user.id)
    return schemas.Response(data=links)


@router.post("/")
async def update_links(
        links: schemas.LinkUpdate,
        user: schemas.UserInfo = Depends(get_current_user),
        db: Session = Depends(get_db)):
    """更新或者插入链接"""
    print(user)
    for i in links.links:
        new_link = schemas.LinkCreate(**i.dict(), user_id=user.user_id)
        crud.link_update_if__exist_or_insert(new_link)
    return schemas.Response()

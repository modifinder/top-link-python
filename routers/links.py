# -*- coding:utf-8 -*-

from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from deps import get_current_user, get_db
import crud
import schemas


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
async def update_links(links: schemas.LinkUpdate, user: schemas.UserInfo = Depends(get_current_user)):
    """更新或者插入链接"""
    for i in links.links:
        new_link = schemas.LinkCreate(**i.dict(), user_id=user.user_id)
        crud.link_update_if__exist_or_insert(new_link)
    return schemas.Response()


@router.delete("/")
async def delete_link_by_lid(data: schemas.StringData, user: schemas.UserInfo = Depends(get_current_user),
                             db: Session = Depends(get_db)):
    """删除一个链接，根据链接的lid"""
    res = crud.delete_link_by_lid(db, data.data)
    print(res)
    return schemas.Response()
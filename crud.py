# -*- coding:utf-8 -*-

from sqlalchemy.orm import Session
import schemas
import models


def get_user_by_user_name(db: Session, user_name: str):
    """ 通过用户名获取用户信息 """
    return db.query(models.User).filter(models.User.user_name == user_name).first()


def create_user(db: Session, user: schemas.UserCreate):
    """ 插入一个新的用户 """
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

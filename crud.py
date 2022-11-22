# -*- coding:utf-8 -*-

from sqlalchemy.orm import Session
from database import engine
from pymysql.converters import escape_string
import schemas
import models


def get_user_by_user_name(db: Session, user_name: str):
    """[Atomic] 通过用户名获取用户信息 """
    return db.query(models.User).filter(models.User.user_name == user_name).first()


def get_user_by_user_id(db: Session, user_id: int):
    """[Atomic] 通过用户id，获取用户信息"""
    return db.query(models.User).filter(models.User.id == user_id).first()


def create_user(db: Session, user: schemas.UserCreate):
    """[Atomic] 插入一个新的用户 """
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_setting_by_user_id(db: Session, user_id: int):
    """[Atomic] 通过 用户id 获取用户设置"""
    return db.query(models.Setting).filter(models.Setting.user_id == user_id).first()


def get_links_by_user_id(db: Session, user_id: int):
    """[Atomic] 通过用户id 获取用户所有链接"""
    return db.query(models.Links).filter(models.Links.user_id == user_id).all()


def get_link_by_link_uuid(db: Session, uuid: str):
    """[Atomic] 通过uuid, 查询对应链接信息"""
    return db.query(models.Links).filter(models.Links.uuid == uuid).first()


def create_link(db: Session, link: schemas.LinkCreate):
    """[Atomic] 添加一个链接"""
    db_link = models.Links(**link.dict())
    db.add(db_link)
    db.commit()
    db.refresh(db_link)
    return db_link


def link_update_if__exist_or_insert(link: schemas.LinkCreate):
    """[Atomic]如果不存在则插入链接，否则更新链接"""
    conn = engine.connect()
    sql = "INSERT INTO links (user_id, `show`, position, uuid, title, url, thumb, type) " \
          "VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s') ON DUPLICATE KEY " \
          "UPDATE title='%s', url='%s', thumb='%s', position='%s', `show`='%s', type='%s';"
    show = 1 if link.show else 0
    res = conn.execute(sql % (link.user_id, show, link.position, escape_string(link.uuid), escape_string(link.title),
                              escape_string(link.url), escape_string(link.thumb), escape_string(link.type),
                              escape_string(link.title), escape_string(link.url), escape_string(link.thumb),
                              link.position, show, escape_string(link.type)))


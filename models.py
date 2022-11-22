# -*- coding:utf-8 -*-

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, CHAR
from sqlalchemy.orm import relationship
from database import Base


class Links(Base):
    """链接"""
    __tablename__ = "links"
    uuid = Column(CHAR(36), primary_key=True, index=True, unique=True)
    user_id = Column(Integer, index=True)
    thumb = Column(String(255))
    title = Column(String(255))
    position = Column(Integer)
    url = Column(String(255))
    show = Column(Boolean, default=False)
    type = Column(String(32), default="default")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String(64), unique=True, index=True)
    email = Column(String(64), index=True)
    hashed_password = Column(String(255))
    enable = Column(Boolean, default=True)
    create_time = Column(Integer)
    update_time = Column(Integer)


class Setting(Base):
    __tablename__ = "setting"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    theme = Column(String(32))
    page_title = Column(String(32))
    page_bio = Column(String(128))
    profile_picture = Column(String(255))

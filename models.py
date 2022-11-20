# -*- coding:utf-8 -*-

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, CHAR
from sqlalchemy.orm import relationship
from database import Base


class Links(Base):
    """链接"""
    __tablename__ = "links"
    uuid = Column(CHAR(32), primary_key=True, index=True)
    thumb = Column(String(255))
    title = Column(String(255))
    position = Column(Integer)
    url = Column(String(255))
    uid = Column(Integer)
    show = Column(Boolean, default=False)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String(64), unique=True, index=True)
    email = Column(String(64), unique=True, index=True)
    hashed_password = Column(String(255))
    profile_picture = Column(String(255))
    page_title = Column(String(32))
    page_bio = Column(String(128))
    create_time = Column(Integer)
    update_time = Column(Integer)

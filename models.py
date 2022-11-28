# -*- coding:utf-8 -*-

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, CHAR
from database import Base


class Links(Base):
    """链接"""
    __tablename__ = "links"
    lid = Column(CHAR(36), primary_key=True, index=True, unique=True)
    user_id = Column(Integer, index=True)
    thumb = Column(String(255))
    title = Column(String(255))
    position = Column(Integer)
    url = Column(String(255))
    display = Column(Boolean, default=False)
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
    verified = Column(Boolean, default=False)
    auth_content = Column(String(128))


class Themes(Base):
    __tablename__ = "theme"
    """
    INSERT INTO `theme` (`id`, `name`, `title`, `has_filter`, `basic_bg`, `title_color`, `bio_color`, `text_color`, `footer_color`, `link_bg`, `link_border_radius`, `thumb_border_radius`, `thumb`) VALUES (NULL, 'yellow', '渐变黄', '0', 'linear-gradient(rgb(255, 240, 3), rgb(255, 126, 23))', '#1d1d1f', '#1d1d1f', '#1d1d1f', '#1d1d1f', 'linear-gradient(rgb(255, 240, 3), rgb(255, 126, 23))', '5px', '5px', '/images/theme/default.jpg')
    """
    id = Column(Integer, primary_key=True, index=True)
    position = Column(Integer)
    display = Column(Boolean)
    name = Column(String(64), index=True)
    title = Column(String(64))
    has_filter = Column(Boolean, default=False)
    basic_bg = Column(String(64))
    title_color = Column(String(64))
    bio_color = Column(String(64))
    text_color = Column(String(64))
    footer_color = Column(String(64))
    link_bg = Column(String(64))
    link_bg_hover = Column(String(64))
    link_border_color = Column(String(64))
    is_link_scale = Column(Boolean, default=True)
    link_border_color_hover = Column(String(64))
    text_color_hover = Column(String(64))
    link_border_radius = Column(String(64))
    thumb_border_radius = Column(String(64))

    thumb = Column(String(128))


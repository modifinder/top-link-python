# -*- coding:utf-8 -*-
import math

from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, func
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


def get_last_insert_id(db: Session):
    """[Atomic] 获取最后一次插入的id"""
    return db.execute("SELECT LAST_INSERT_ID()").fetchone()[0]


def create_user(db: Session, user: schemas.UserCreate):
    """[Atomic] 插入一个新的用户 """
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    last_id = get_last_insert_id(db)
    return last_id


def create_setting(db: Session, setting: schemas.SettingCreate):
    """[Atomic] 插入一个新的用户设置"""
    db_setting = models.Setting(**setting.dict())
    db.add(db_setting)
    db.commit()
    db.refresh(db_setting)
    return db_setting


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


def delete_link_by_lid(db: Session, link_id: str):
    """[Atomic] 根据lid删除一个链接"""
    db.query(models.Links).filter(models.Links.lid == link_id).delete()
    db.commit()
    return


def link_update_if__exist_or_insert(link: schemas.LinkCreate):
    """[Atomic]如果不存在则插入链接，否则更新链接"""
    conn = engine.connect()
    sql = "INSERT INTO links (user_id, `display`, position, lid, title, url, thumb, type) " \
          "VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s') ON DUPLICATE KEY " \
          "UPDATE title='%s', url='%s', thumb='%s', position='%s', `display`='%s', type='%s';"
    display = 1 if link.display else 0
    res = conn.execute(sql % (link.user_id, display, link.position, escape_string(link.lid), escape_string(link.title),
                              escape_string(link.url), escape_string(link.thumb), escape_string(link.type),
                              escape_string(link.title), escape_string(link.url), escape_string(link.thumb),
                              link.position, display, escape_string(link.type)))


def fetch_themes(db: Session):
    """[Atomic]"""
    return db.query(models.Themes).filter().all()


def get_theme_by_theme_name(db: Session, theme_name: str):
    """[Atomic] 根据主题名，获取主题信息"""
    return db.query(models.Themes).filter(models.Themes.name == theme_name).first()


def set_setting_theme_by_user_id(db: Session, user_id: int, theme_name: str):
    """[Atomic] 根据用户id，设置用户主题"""
    setting = db.query(models.Setting).filter(models.Setting.user_id == user_id).first()
    setting.theme = theme_name
    db.commit()
    return


def set_setting_base_by_user_id(db: Session, user_id: int, data: schemas.SettingBase):
    """
    设置一些基础信息，包括标题、简介和头像
    :param db:
    :param user_id:
    :param data:
    :return:
    """
    setting = db.query(models.Setting).filter(models.Setting.user_id == user_id).first()
    setting.page_title = data.page_title
    setting.page_bio = data.page_bio
    setting.profile_picture = data.profile_picture
    db.commit()
    return


def get_all_fields(db: Session):
    """[Atomic] 获取所有人群信息"""
    return db.query(models.Field).filter().all()


def get_all_interest_primary(db: Session):
    """[Atomic] 获取所有主要兴趣信息"""
    return db.query(models.InterestPrimary).filter().all()


def get_setting_by_interest_code_and_field_code(db: Session, field_code: int = 0, interest_code: int = 0,
                                                page: int = 1, page_size: 0 = 0):
    """根据领域或者兴趣id查询用户的信息"""
    query = db.query(models.Setting)

    # 限制每页最大数据量
    if page_size > 50:
        page_size = 10

    offset = (page - 1) * page_size
    if field_code and interest_code:
        data = query.filter(
            and_(models.Setting.field_code == field_code, models.Setting.interest_primary_code == interest_code)
        ).limit(page_size).offset(offset).all()
        count = db.query(func.count(models.Setting.id)).filter(
            models.Setting.field_code == field_code,
            models.Setting.interest_primary_code == interest_code
        ).scalar()
        pages = math.ceil(count / page_size)
        return data, pages
    elif field_code and not interest_code:
        data = query.filter(models.Setting.field_code == field_code).limit(page_size).offset(offset).all()
        count = db.query(func.count(models.Setting.field_code)).filter(models.Setting.field_code == field_code).scalar()
        pages = math.ceil(count / page_size)
        return data, pages
    elif not field_code and interest_code:
        data = query.filter(models.Setting.interest_primary_code == interest_code).limit(page_size).offset(offset).all()
        count = db.query(func.count(models.Setting.interest_primary_code)).filter(
            models.Setting.interest_primary_code == interest_code
        ).scalar()
        pages = math.ceil(count / page_size)
        return data, pages
    return None, 0


def explore_setting(db: Session, field_code: int = 0, tags: List = [], page: int = 10, limit: int = 1):
    """根据field_code以及tags查询用户信息"""
    query = db.query(models.Setting)

    # The max limit is 50
    if limit > 50:
        limit = 10

    offset = (page - 1) * limit

    # Case 1: only field_code
    if field_code and not len(tags):
        data = query.filter(models.Setting.field_code == field_code).limit(limit).offset(offset).all()
        count = db.query(func.count(models.Setting.field_code)).filter(models.Setting.field_code == field_code).scalar()
        pages = math.ceil(count / limit)
        return data, pages


    # Case 2: only tags
    elif not field_code and tags:
        tags_id = []
        for i in tags:
            data = get_tag_id_by_tag_name(db, i)
            if data:
                tags_id.append(data.id)
        users_id = db.query(models.UserTag.user_id).filter(models.UserTag.tag_id.in_(tags_id)).distinct(models.UserTag.user_id).all()
        users_id = [i[0] for i in users_id if any(i)]
        data = query.filter(models.Setting.user_id.in_(users_id)).limit(limit).offset(offset).all()
        count = db.query(func.count(models.Setting.user_id)).filter(models.Setting.user_id.in_(users_id)).scalar()
        return data, math.ceil(count / limit)

    # Case 3: field_code and tags
    tags_id = []
    for i in tags:
        data = get_tag_id_by_tag_name(db, i)
        if data:
            tags_id.append(data.id)
    users_id = db.query(models.UserTag.user_id).filter(models.UserTag.tag_id.in_(tags_id)).distinct(models.UserTag.user_id).all()
    users_id = [i[0] for i in users_id if any(i)]
    data = query.filter(models.Setting.user_id.in_(users_id), models.Setting.field_code == field_code).limit(limit).offset(offset).all()
    count = db.query(func.count(models.Setting.user_id)).filter(models.Setting.user_id.in_(users_id), models.Setting.field_code == field_code).scalar()
    return data, math.ceil(count / limit)



def get_all_icons(db: Session):
    """[Atomic] 获取所有图标信息"""
    return db.query(models.Icon).filter().all()


def get_default_tags(db: Session, is_english: bool = False):
    """获取默认标签组"""
    if is_english:
        return db.query(models.Tag).offset(12).limit(12).all()
    return db.query(models.Tag).limit(12).all()


def get_tag_id_by_tag_name(db: Session, tag_name: str):
    """根据标签名获取标签id"""
    return db.query(models.Tag).filter(models.Tag.name == tag_name).first()


def add_one_tag_by_tag_name(db: Session, tag_name: str):
    """添加一个标签"""
    tag = models.Tag(name=tag_name)
    db.add(tag)
    db.commit()
    db.refresh(tag)
    return tag


def add_user_tag(db: Session, user_id: int, tag_id: int):
    """添加用户标签"""
    user_tag = models.UserTag(user_id=user_id, tag_id=tag_id)
    db.add(user_tag)
    db.commit()
    db.refresh(user_tag)
    return user_tag


def is_sensitive_word(db: Session, word: str):
    """判断是否是敏感词"""
    return db.query(models.SensitiveWord).filter(models.SensitiveWord.word == word).first()
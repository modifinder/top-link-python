# -*- coding:utf-8 -*-

from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session


from deps import get_current_user, get_db
import crud
import schemas
import models

router = APIRouter()


@router.get("/explore")
async def get_setting_explore(db: Session = Depends(get_db), field_code: int = 0, interest_code: int = 0,
                              page: int = 1, limit: int = 15):
    """根据领域和兴趣来查找用户"""
    result, count = crud.get_setting_by_interest_code_and_field_code(db, field_code, interest_code, page, limit)
    return schemas.ResponseWithCount(data=result, count=count)


@router.get("/fields")
async def get_setting_fields(db: Session = Depends(get_db)):
    """
    获取用户设置的字段
    :param db:
    :return:
    """
    fields = crud.get_all_fields(db)
    if not fields:
        raise HTTPException(
            status_code=500,
            detail="an error occurred"
        )
    return schemas.Response(data=fields)


@router.get("/interest/primary")
async def get_all_interest_primary(db: Session = Depends(get_db)):
    """
    获取所有的一级兴趣
    :param db:
    :return:
    """
    interest = crud.get_all_interest_primary(db)
    if not interest:
        raise HTTPException(
            status_code=500,
            detail="an error occurred"
        )
    return schemas.Response(data=interest)


@router.get("/user/{username}")
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


@router.patch("/theme/{theme}")
async def set_user_theme_by_user_id(db: Session = Depends(get_db), theme: str = "default",
                                    user: schemas.UserInfo = Depends(get_current_user)):
    """设置用户主题"""
    allow_theme = [i for i in crud.fetch_themes(db) if i.name == theme]
    if allow_theme and allow_theme[0].display:
        crud.set_setting_theme_by_user_id(db, user.user_id, theme)
        return schemas.Response()
    raise HTTPException(
        status_code=400,
        detail="Not allow setting this theme"
    )


@router.patch("/base")
async def patch_setting_base(setting: schemas.SettingBase,
                        user: schemas.UserInfo = Depends(get_current_user),
                        db: Session = Depends(get_db)):
    """
    :param db:
    :param setting:
    :param user: deps
    :return:
    """
    try:
        crud.set_setting_base_by_user_id(db, user.user_id, setting)
        return schemas.Response()
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500,
            detail="an error occurred"
        )


@router.get("/tags/default/{_type}")
async def get_default_tags(db: Session = Depends(get_db), _type: str = "zh"):
    """
    get the default tags
    :param db:
    :return:
    """
    is_english = True if _type == "en" else False
    tags = crud.get_default_tags(db, is_english)
    return schemas.Response(data=tags)
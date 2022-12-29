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
from utils import get_retain_username
router = APIRouter()


@router.post('/signup', summary="Create new user")
async def create_user(data: schemas.UserRegister, db: Session = Depends(get_db)):
    print(data.dict())
    # check username if it exited
    user = crud.get_user_by_user_name(db, data.user_name)
    if user is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this name already exist"
        )


    hashed_password = get_hashed_password(data.password)
    new_user = data.dict()
    del new_user['password']
    new_user['hashed_password'] = hashed_password
    now = int(time.time())

    try:
        # create user
        user_create = schemas.UserCreate(**new_user, enable=True, create_time=now, update_time=now)
        crud.create_user(db, user_create)
        user_id = crud.get_user_by_user_name(db, data.user_name).id

        # create user setting
        setting_create = schemas.SettingCreate(
            user_id=user_id, user_name=data.user_name, page_title="@"+data.user_name,
            field_code = data.field_code
        )
        crud.create_setting(db, setting_create)


        # insert user tags
        tags = data.tags
        for tag in tags:
            # check tag if it exited
            tag_id = crud.get_tag_id_by_tag_name(db, tag)
            if not tag_id:
                # create new tag
                crud.add_one_tag_by_tag_name(db, tag)
                tag_id = crud.get_tag_id_by_tag_name(db, tag)
            crud.add_user_tag(db, user_id, tag_id.id)


        # return
        return schemas.Response(msg="user created successfully", data={
            "access_token": create_access_token(data.user_name),
            "refresh_token": create_refresh_token(data.user_name),
        })

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post('/login', summary="Create access and refresh tokens for user")
async def login(user: schemas.UserAuth, db: Session = Depends(get_db)):
    # user = db.get(form_data.username, None)
    data = crud.get_user_by_user_name(db, user.user_name)
    if data is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )

    if not verify_password(user.password, data.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )

    return schemas.Response(data={
        "access_token": create_access_token(user.user_name),
        "refresh_token": create_refresh_token(user.user_name),
    })


@router.get('/me', summary='Get details of currently logged in user')
async def get_me(user: schemas.UserBase = Depends(get_current_user)):
    return schemas.Response(data=user.dict())


@router.get("/exists/{username}", summary="Check if user exists")
async def check_user_exists(username: str, db: Session = Depends(get_db)):
    # 检查是否保留用户名
    for i in get_retain_username():
        if i == username:
            return schemas.Response(data=True)

    user = crud.get_user_by_user_name(db, username)
    return schemas.Response(data=user is not None)


# -*- coding:utf-8 -*-

import time
from fastapi import FastAPI, status, HTTPException, Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
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


@router.post('/signup', summary="Create new user")
async def create_user(data: schemas.UserAuth, db: Session = Depends(get_db)):
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
    user_create = schemas.UserCreate(**new_user, enable=True, create_time=now, update_time=now)
    crud.create_user(db, user_create)
    return schemas.Response(msg="user created successfully")


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

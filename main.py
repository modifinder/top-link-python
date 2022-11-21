# -*- coding:utf-8 -*-

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
import models
import schemas
from database import SessionLocal, engine
from routers import user, upload

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(
    user.router,
    prefix="/user",
    tags=["user"]
)

app.include_router(
    upload.router,
    prefix="/upload",
    tags=["upload"]
)


@app.get("/")
async def get_root():
    return schemas.Response()


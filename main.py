# -*- coding:utf-8 -*-

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
import models
import schemas
from database import SessionLocal, engine
from routers import user

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(
    user.router,
    prefix="/user",
    tags=["user"]
)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def get_root():
    return schemas.Response()


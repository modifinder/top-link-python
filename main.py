# -*- coding:utf-8 -*-

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import models
import schemas
from database import engine
from routers import user, upload, setting, links, theme

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "https://the.top",
    "https://www.the.top",
    "https://test.5050520.xyz",
    "http://localhost",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(
    user.router,
    prefix="/user",
    tags=["user"]
)


app.include_router(
    links.router,
    prefix="/links",
    tags=["links"]
)


app.include_router(
    upload.router,
    prefix="/upload",
    tags=["upload"]
)

app.include_router(
    setting.router,
    prefix="/setting",
    tags=["setting"]
)

app.include_router(
    theme.router,
    prefix="/theme",
    tags=["theme"]
)


@app.get("/")
async def get_root():
    return schemas.Response()


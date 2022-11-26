# -*- coding:utf-8 -*-


from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from deps import get_current_user, get_db
import crud
import schemas
import models

router = APIRouter()


@router.get("/all")
async def get_themes(db: Session = Depends(get_db)):
    return schemas.Response(data=crud.fetch_themes(db))


@router.get("/{theme_name}")
async def get_theme_by_theme_name(theme_name: str, db: Session = Depends(get_db)):
    return schemas.Response(data=crud.get_theme_by_theme_name(db, theme_name))

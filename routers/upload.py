# -*- coding: utf-8 -*-

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import crud
import schemas
import uuid
from deps import get_current_user, get_db
import utils

router = APIRouter()


@router.post("/images/{sub_dir}")
async def upload_avatar(sub_dir: str, data: schemas.UploadImage, user: schemas.UserBase = Depends(get_current_user)):

    if sub_dir not in ["thumb", "avatar"]:
        raise HTTPException(
            status_code=400,
            detail="sub_dir is not allowed"
        )

    old_file_name = data.origin.split("/")[-1]
    new_file_name = user.user_name + "-" + str(uuid.uuid4()) + ".jpg"
    print(new_file_name, old_file_name)
    # 系统默认的图片(头像)不用删
    if "default" not in old_file_name:
        ok, msg = utils.delete_image_from_cos(old_file_name, sub_dir)
        print(ok, msg)
        if not ok:
            raise HTTPException(status_code=502, detail=msg)

    ok, msg = utils.put_image_to_cos(new_file_name, data.image_b64, sub_dir)
    if not ok:
        raise HTTPException(status_code=502, detail=msg)
    return schemas.Response(data={"file_name": msg})




@router.delete("/images/thumb")
async def delete_icon(data: schemas.StringData, user: schemas.UserBase = Depends(get_current_user)):
    """删除图标
        [Todo] 需要加上删除鉴定
    """
    file_name = data.data.split("/")[-1]
    utils.delete_image_from_cos(file_name, "thumb")
    return schemas.Response()



@router.get("/icon")
async def get_icon(db: Session =  Depends(get_db)):
    """获取图标"""
    return schemas.Response(data=crud.get_all_icons(db))
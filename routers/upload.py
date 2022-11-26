# -*- coding: utf-8 -*-

from fastapi import APIRouter, Depends
import schemas
import base64
import uuid
from deps import get_current_user
import os

router = APIRouter()


@router.post("/icon")
async def upload_icon(data: schemas.UploadThumb, user: schemas.UserBase = Depends(get_current_user)):
    base_path = "/Users/mac/JavaScriptProjects/top-bio/public/images/thumb"

    try:
        file_name = data.origin.split("/")[-1]
        origin_path = f"{base_path}/{file_name}"

        # 删除旧图片
        if data.origin != "/images/thumb.jpg" and os.path.isfile(origin_path):
            os.remove(origin_path)
    except Exception as e:
        print(e)

    # 保存新图片
    head, content = data.image_b64.split(",")
    file_name = user.user_name + "-" + str(uuid.uuid4()) + ".jpg"
    img_data = base64.b64decode(content)
    with open(f"{base_path}/{file_name}", "wb") as f:
        f.write(img_data)
    return schemas.Response(data={"file_name": file_name})


@router.delete("/icon")
async def delete_icon(data: schemas.StringData, user: schemas.UserBase = Depends(get_current_user)):
    """删除图标"""
    base_path = "/Users/mac/JavaScriptProjects/top-bio/public/images/thumb"
    try:
        file_name = data.data.split("/")[-1]
        origin_path = f"{base_path}/{file_name}"
        # 删除旧图片
        if data.data != "/images/thumb.jpg" and os.path.isfile(origin_path):
            os.remove(origin_path)
    except Exception as e:
        print(e)
    return schemas.Response()
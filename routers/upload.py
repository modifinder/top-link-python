# -*- coding: utf-8 -*-

from fastapi import APIRouter, Depends
import schemas
import base64
import uuid
from deps import get_current_user

router = APIRouter()


@router.post("/icon")
async def upload_icon(data: schemas.StringData, user: schemas.UserBase = Depends(get_current_user)):
    head, content = data.data.split(",")
    file_name = user.user_name + "-" + str(uuid.uuid4()) + ".jpg"
    img_data = base64.b64decode(content)
    with open(f"/Users/mac/JavaScriptProjects/top-bio/public/images/thumb/{file_name}", "wb") as f:
        f.write(img_data)
    return schemas.Response(data={"file_name": file_name})

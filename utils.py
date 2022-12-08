from passlib.context import CryptContext
import os
import base64
from datetime import datetime, timedelta
from typing import Union, Any
from jose import jwt
import re


ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 14  # 14 days
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 14  # 14 days
ALGORITHM = "HS256"
JWT_SECRET_KEY = "10ds5e0j4saa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e813e7"
JWT_REFRESH_SECRET_KEY = "09d25e094faa6ca2556cl181h6bha95hhh93f209926f0f1caa6c163b88e8d3e7"
images_base_path = "/Users/mac/JavaScriptProjects/top-bio/public/images"

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)


def create_access_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)
    return encoded_jwt


def create_refresh_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_REFRESH_SECRET_KEY, ALGORITHM)
    return encoded_jwt


def create_image(sub_dir: str, file_name: str, image_data: str):
    """
    :return:
    """
    head, content = image_data.split(",")
    img_data = base64.b64decode(content)

    try:
        with open(f"{images_base_path}/{sub_dir}/{file_name}", "wb+") as f:
            f.write(img_data)
        return True, ""
    except Exception as e:
        return False, e


def delete_image_by_filename(sub_dir: str, file_name: str):
    """
    :param
        :file_name 文件名
    删除旧文件
    :return:
    """
    path = f"{images_base_path}/{sub_dir}/{file_name}"
    try:
        if os.path.isfile(path):
            os.remove(path)
        return True, ""
    except Exception as e:
        return False, e


def get_retain_username() -> str:
    """
    获取保留用户名
    :return:
    """
    retain_username = ["admin", "administrator", "root", "superuser", "super", "user", "guest",
                       "anonymous", "anonymoususer", "anonymous_user"]
    return retain_username


def is_email(email: str) -> bool:
    """
    判断是否为邮箱
    :param email:
    :return:
    """
    if len(email) > 7:
        if re.match("^.+@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) is not None:
            return True
    return False


def is_username(username: str) -> bool:
    """
    判断是否为用户名
    :param username:
    :return:
    """
    if re.match("^[a-zA-Z0-9_-]{4,16}$", username) is not None:
        return True
    return False

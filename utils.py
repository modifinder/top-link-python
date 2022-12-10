# -*- coding=utf-8

from passlib.context import CryptContext
import os
import base64
from datetime import datetime, timedelta
from typing import Union, Any
from jose import jwt
import re

from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
import sys
import logging

# 正常情况日志级别使用INFO，需要定位时可以修改为DEBUG，此时SDK会打印和服务端的通信信息
logging.basicConfig(level=logging.INFO, stream=sys.stdout)

# 1. 设置用户属性, 包括 secret_id, secret_key, region等。Appid 已在CosConfig中移除，请在参数 Bucket 中带上 Appid。Bucket 由 BucketName-Appid 组成
secret_id = os.getenv("cos_app_id")
secret_key = os.getenv("cos_app_key")
region = 'ap-shanghai'

token = None
scheme = 'https'

config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token, Scheme=scheme)
client = CosS3Client(config)

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 14  # 14 days
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 14  # 14 days
ALGORITHM = "HS256"
JWT_SECRET_KEY = os.getenv("jwt_key")
JWT_REFRESH_SECRET_KEY = os.getenv("jwt_refresh_key")

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


def get_retain_username() -> str:
    """
    获取保留用户名
    :return:
    """
    retain_username = ["admin", "administrator", "root", "superuser", "super", "user", "guest",
                       "anonymous", "anonymoususer", "anonymous_user", "test", "testuser", "test_user",
                       ]
    return retain_username


def is_email(email: str) -> bool:
    """
    判断是否为邮箱
    :param email:
    :return:
    """
    if re.match(r"^(([^<>()\[\]\\.,;:\s@']+(\.[^<>()\[\]\\.,;:\s@']+)*)|('.+'))@((\[[0-9]{1,3}\.[0-9]{1,"
                r"3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$", email) is not None:
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


def put_image_to_cos(file_name: str, image_data: str, sub_dir: str = "avatar"):
    """
    :return:
    """
    head, content = image_data.split(",")
    img_data = base64.b64decode(content)
    sub_dir = f"/top/images/{sub_dir}"
    key = f"{sub_dir}/{file_name}"
    try:
        response = client.put_object(
            Bucket='top-bio-1308265831',
            Body=img_data,
            Key=key,
            StorageClass='STANDARD',
            EnableMD5=False
        )
        print(response)
        return True, key
    except Exception as e:
        print(response)
        return False, e


def delete_image_from_cos(file_name: str, sub_dir: str = "avatar"):
    """
    :param
        :file_name 文件名
    删除旧文件
    :return:
    """
    sub_dir = f"/top/images/{sub_dir}"
    key = f"{sub_dir}/{file_name}"
    print(key, "keykeykeykye")
    try:
        response = client.delete_object(
            Bucket='top-bio-1308265831',
            Key=key
        )
        return True, key
    except Exception as e:
        return False, e

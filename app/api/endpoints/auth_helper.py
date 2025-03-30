import hashlib
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path
from uuid import uuid4

import dotenv
import jwt
from fastapi import HTTPException
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

from app import models
from app.crud.user_crud import UserCrud

dotenv.load_dotenv()


def get_envfile_path() -> str:
    return (Path(__file__) / "../../../.env").resolve().as_posix()


class JWTConfig(BaseSettings):
    secret_key: str
    algorithm: str
    expires_delta: int

    model_config = SettingsConfigDict(
        env_prefix="JWT_",
        extra="ignore",
        env_file=get_envfile_path(),
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


class JWTer:
    config: JWTConfig

    def __init__(self, config: JWTConfig = JWTConfig()):
        self.config = config

    @staticmethod
    def expires_timestamp(expires_delta: int):
        expires_at = datetime.now(timezone.utc) + timedelta(minutes=expires_delta)
        return int(datetime.timestamp(expires_at))

    def encode(self, payload) -> str:
        return jwt.encode(payload, self.config.secret_key, self.config.algorithm)

    def decode(self, token: str) -> any:
        try:
            payload = jwt.decode(token, self.config.secret_key, self.config.algorithm)
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="token has been expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="invalid token")
        except Exception as e:
            raise e


def get_jwter() -> JWTer:
    return JWTer()


class PasswordConfig(BaseSettings):
    salt: str
    pepper: str

    model_config = SettingsConfigDict(
        env_prefix="PASSWORD_",
        extra="ignore",
        env_file=get_envfile_path(),
        env_ignore_empty=True,
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


class PasswordHasher:
    config: PasswordConfig

    def __init__(self, config: PasswordConfig = PasswordConfig()):
        self.config = config

    def hash_password(self, password: str | SecretStr) -> str:
        if isinstance(password, SecretStr):
            password = password.get_secret_value()
        password_with_salt = self.config.salt + password
        hashed = hashlib.sha256(password_with_salt.encode("utf-8")).hexdigest()
        return hashed  # TODO


async def get_password_hasher() -> PasswordHasher:
    return PasswordHasher()


def generate_access_token(jwter: JWTer, user: models.User) -> str:
    payload = {
        "sub": user.id,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=300),
    }
    return jwter.encode(payload)

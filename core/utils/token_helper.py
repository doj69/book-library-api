from datetime import datetime, timedelta
from typing import Mapping, NoReturn

import jwt

from core.config import config
from core.exceptions import DecodeTokenException, ExpiredTokenException


class TokenHelper:
    @staticmethod
    def encode(payload: dict, expire_period: int = 3600) -> str:
        token = jwt.encode(
            payload={
                **payload,
                "exp": datetime.utcnow() + timedelta(seconds=expire_period),
            },
            key=config.JWT_SECRET_KEY,
            algorithm=config.JWT_ALGORITHM,
        ).decode("utf8")
        return token

    @staticmethod
    def decode(token: str) -> Mapping[dict, NoReturn]:
        try:
            return jwt.decode(
                jwt=token, key=config.JWT_SECRET_KEY, algorithms=[config.JWT_ALGORITHM]
            )
        except jwt.exceptions.DecodeError:
            raise DecodeTokenException
        except jwt.exceptions.ExpiredSignatureError:
            raise ExpiredTokenException

    @staticmethod
    def decode_expired_token(token: str) -> Mapping[dict, NoReturn]:
        try:
            return jwt.decode(
                jwt=token, key=config.JWT_SECRET_KEY, algorithms=[config.JWT_ALGORITHM]
            )
        except jwt.exceptions.DecodeError:
            raise DecodeTokenException

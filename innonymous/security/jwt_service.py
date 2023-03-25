import json
from typing import TypeVar

import jwt
from pydantic import BaseModel

from innonymous.security.expiration_time import ExpirationTime


class JwtService:
    PayloadModel = TypeVar("PayloadModel", bound=BaseModel)

    def __init__(self, key: str, ttl_seconds: int, algorithm: str = "HS256") -> None:
        self.__key = key
        self.__algorithm = algorithm
        self.__expiration_time = ExpirationTime(ttl_seconds)

    @property
    def expiration_time(self) -> ExpirationTime:
        return self.__expiration_time

    def encode(self, payload: PayloadModel) -> str:
        payload = json.loads(payload.json())

        return jwt.encode(payload, self.__key, self.__algorithm)

    def decode(self, token: str, model: type[PayloadModel]) -> PayloadModel:
        return model.parse_obj(
            jwt.decode(
                token,
                self.__key,
                [
                    self.__algorithm,
                ],
            )
        )

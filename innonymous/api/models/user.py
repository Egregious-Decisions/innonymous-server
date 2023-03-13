from uuid import UUID

from pydantic import BaseModel, Field


class User(BaseModel):
    uuid: UUID = Field(...)
    nickname: str = Field(...)

    chat_rooms: list[UUID] = Field(default_factory=list)

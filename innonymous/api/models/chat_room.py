from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class ChatRoom(BaseModel):
    uuid: UUID = Field(...)
    creator_uuid: UUID = Field(...)
    created_at: datetime = Field(...)
    name: str = Field(...)
    messages: list[UUID]

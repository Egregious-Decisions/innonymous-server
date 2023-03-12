from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, Field


class Message(BaseModel):
    uuid: UUID = Field(...)
    chat_room_uuid: UUID = Field(...)
    sender_uuid: UUID = Field(...)
    date: datetime = Field(...)
    text: str = Field(...)

    reply_to: UUID | None = Field(None)

from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class MessageResponse(BaseModel):
    id: str
    chat_id: str
    direction: str
    text: str
    telegram_message_id: Optional[int] = None
    sent_by_user_id: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class SendMessageRequest(BaseModel):
    text: str

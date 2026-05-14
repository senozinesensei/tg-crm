from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.schemas.contact import ContactResponse


class ChatResponse(BaseModel):
    id: str
    contact_id: str
    last_message_text: Optional[str] = None
    last_message_at: Optional[datetime] = None
    unread_count: int = 0
    created_at: datetime
    contact: Optional[ContactResponse] = None

    class Config:
        from_attributes = True

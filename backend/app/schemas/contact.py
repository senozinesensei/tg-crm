from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ContactResponse(BaseModel):
    id: str
    telegram_id: int
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None
    avatar_url: Optional[str] = None
    created_at: datetime
    last_activity_at: datetime

    class Config:
        from_attributes = True

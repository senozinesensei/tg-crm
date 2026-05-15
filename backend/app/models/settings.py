import uuid
from datetime import datetime
from sqlalchemy import Integer, String, Boolean, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class Settings(Base):
    __tablename__ = "settings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, default=1)
    bot_token: Mapped[str | None] = mapped_column(String(255), nullable=True)
    webhook_url: Mapped[str | None] = mapped_column(String(512), nullable=True)
    webhook_active: Mapped[bool] = mapped_column(Boolean, default=False)
    openrouter_api_key: Mapped[str | None] = mapped_column(String(512), nullable=True)
    openrouter_model: Mapped[str] = mapped_column(String(255), default="openai/gpt-4o-mini")
    openrouter_system_prompt: Mapped[str] = mapped_column(
        Text,
        default="You are a helpful Telegram support assistant. Reply clearly and concisely.",
    )
    openrouter_history_limit: Mapped[int] = mapped_column(Integer, default=10)
    ai_auto_reply_enabled: Mapped[bool] = mapped_column(Boolean, default=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

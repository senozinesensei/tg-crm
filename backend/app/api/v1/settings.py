from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from typing import Optional
from app.database import get_db
from app.models.settings import Settings
from app.models.user import User
from app.api.deps import get_current_user
from app.services.telegram_service import (
    register_webhook,
    delete_webhook,
    get_webhook_info,
)
from datetime import datetime

router = APIRouter(prefix="/settings", tags=["settings"])


class SettingsResponse(BaseModel):
    bot_token_set: bool
    bot_token_masked: Optional[str] = None
    webhook_url: Optional[str] = None
    webhook_active: bool = False
    openrouter_api_key_set: bool = False
    openrouter_api_key_masked: Optional[str] = None
    openrouter_model: str = "openai/gpt-4o-mini"
    openrouter_system_prompt: str = "You are a helpful Telegram support assistant. Reply clearly and concisely."
    openrouter_history_limit: int = 10
    ai_auto_reply_enabled: bool = False

    class Config:
        from_attributes = True


class BotTokenUpdate(BaseModel):
    bot_token: str


class WebhookRegister(BaseModel):
    webhook_url: str


class OpenRouterSettingsUpdate(BaseModel):
    openrouter_api_key: Optional[str] = None
    openrouter_model: str
    openrouter_system_prompt: str
    openrouter_history_limit: int
    ai_auto_reply_enabled: bool


def mask_secret(value: Optional[str]) -> Optional[str]:
    if not value:
        return None
    if len(value) <= 12:
        return value[:4] + "..."
    return value[:8] + "..." + value[-4:]


async def get_or_create_settings(db: AsyncSession) -> Settings:
    result = await db.execute(select(Settings).where(Settings.id == 1))
    settings = result.scalar_one_or_none()
    if not settings:
        settings = Settings(id=1)
        db.add(settings)
        await db.flush()
    return settings


@router.get("", response_model=SettingsResponse)
async def get_settings(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    settings = await get_or_create_settings(db)
    return SettingsResponse(
        bot_token_set=bool(settings.bot_token),
        bot_token_masked=mask_secret(settings.bot_token),
        webhook_url=settings.webhook_url,
        webhook_active=settings.webhook_active,
        openrouter_api_key_set=bool(settings.openrouter_api_key),
        openrouter_api_key_masked=mask_secret(settings.openrouter_api_key),
        openrouter_model=settings.openrouter_model,
        openrouter_system_prompt=settings.openrouter_system_prompt,
        openrouter_history_limit=settings.openrouter_history_limit,
        ai_auto_reply_enabled=settings.ai_auto_reply_enabled,
    )


@router.put("/bot-token")
async def update_bot_token(
    data: BotTokenUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    settings = await get_or_create_settings(db)
    settings.bot_token = data.bot_token
    settings.updated_at = datetime.utcnow()
    return {"status": "ok", "message": "Bot token updated"}


@router.put("/openrouter")
async def update_openrouter_settings(
    data: OpenRouterSettingsUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if data.openrouter_history_limit < 1 or data.openrouter_history_limit > 50:
        raise HTTPException(status_code=400, detail="History limit must be between 1 and 50")
    if not data.openrouter_model.strip():
        raise HTTPException(status_code=400, detail="OpenRouter model is required")
    if not data.openrouter_system_prompt.strip():
        raise HTTPException(status_code=400, detail="System prompt is required")

    settings = await get_or_create_settings(db)
    api_key = data.openrouter_api_key.strip() if data.openrouter_api_key else ""
    if api_key:
        settings.openrouter_api_key = api_key
    settings.openrouter_model = data.openrouter_model.strip()
    settings.openrouter_system_prompt = data.openrouter_system_prompt.strip()
    settings.openrouter_history_limit = data.openrouter_history_limit
    settings.ai_auto_reply_enabled = data.ai_auto_reply_enabled
    settings.updated_at = datetime.utcnow()
    return {"status": "ok", "message": "OpenRouter settings updated"}


@router.post("/webhook/register")
async def register_webhook_endpoint(
    data: WebhookRegister,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    settings = await get_or_create_settings(db)
    if not settings.bot_token:
        raise HTTPException(status_code=400, detail="Bot token is not set")

    webhook_url = data.webhook_url.rstrip("/") + "/webhook/telegram"
    success = await register_webhook(settings.bot_token, webhook_url)
    if not success:
        raise HTTPException(status_code=502, detail="Failed to register webhook with Telegram")

    settings.webhook_url = data.webhook_url
    settings.webhook_active = True
    settings.updated_at = datetime.utcnow()
    return {"status": "ok", "message": "Webhook registered", "webhook_url": webhook_url}


@router.delete("/webhook")
async def delete_webhook_endpoint(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    settings = await get_or_create_settings(db)
    if not settings.bot_token:
        raise HTTPException(status_code=400, detail="Bot token is not set")

    success = await delete_webhook(settings.bot_token)
    if not success:
        raise HTTPException(status_code=502, detail="Failed to delete webhook")

    settings.webhook_active = False
    settings.updated_at = datetime.utcnow()
    return {"status": "ok", "message": "Webhook deleted"}


@router.get("/webhook/status")
async def webhook_status(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    settings = await get_or_create_settings(db)
    if not settings.bot_token:
        return {"active": False, "url": None, "info": None}

    info = await get_webhook_info(settings.bot_token)
    return {
        "active": settings.webhook_active,
        "url": settings.webhook_url,
        "info": info,
    }

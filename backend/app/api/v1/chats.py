from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from typing import List
from app.database import get_db
from app.models.chat import Chat
from app.models.message import Message
from app.models.user import User
from app.schemas.chat import ChatResponse
from app.schemas.message import MessageResponse, SendMessageRequest
from app.api.deps import get_current_user
from app.services.telegram_service import send_telegram_message
from app.services.chat_service import get_bot_token
from app.websocket.manager import manager
from datetime import datetime
import uuid

router = APIRouter(prefix="/chats", tags=["chats"])


@router.get("", response_model=List[ChatResponse])
async def get_chats(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(Chat)
        .options(joinedload(Chat.contact))
        .order_by(Chat.last_message_at.desc().nullslast())
    )
    chats = result.scalars().unique().all()
    return chats


@router.get("/{chat_id}", response_model=ChatResponse)
async def get_chat(
    chat_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(Chat).options(joinedload(Chat.contact)).where(Chat.id == chat_id)
    )
    chat = result.scalar_one_or_none()
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    return chat


@router.get("/{chat_id}/messages", response_model=List[MessageResponse])
async def get_chat_messages(
    chat_id: str,
    limit: int = 50,
    offset: int = 0,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(Message)
        .where(Message.chat_id == chat_id)
        .order_by(Message.created_at.asc())
        .offset(offset)
        .limit(limit)
    )
    messages = result.scalars().all()
    return messages


@router.post("/{chat_id}/messages", response_model=MessageResponse)
async def send_message(
    chat_id: str,
    data: SendMessageRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(Chat).options(joinedload(Chat.contact)).where(Chat.id == chat_id)
    )
    chat = result.scalar_one_or_none()
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")

    bot_token = await get_bot_token(db)
    if not bot_token:
        raise HTTPException(status_code=400, detail="Bot token is not configured")

    telegram_response = await send_telegram_message(
        bot_token=bot_token,
        chat_id=chat.contact.telegram_id,
        text=data.text,
    )

    if not telegram_response:
        raise HTTPException(status_code=502, detail="Failed to send message to Telegram")

    message = Message(
        id=str(uuid.uuid4()),
        chat_id=chat_id,
        direction="outgoing",
        text=data.text,
        telegram_message_id=telegram_response.get("message_id"),
        sent_by_user_id=current_user.id,
        created_at=datetime.utcnow(),
    )
    db.add(message)

    chat.last_message_text = data.text
    chat.last_message_at = message.created_at
    await db.flush()

    msg_data = MessageResponse.model_validate(message).model_dump(mode="json")
    await manager.broadcast({
        "type": "new_message",
        "data": msg_data,
    })
    await manager.broadcast({
        "type": "chat_updated",
        "data": {
            "chat_id": chat_id,
            "last_message_text": chat.last_message_text,
            "last_message_at": chat.last_message_at.isoformat() if chat.last_message_at else None,
            "unread_count": chat.unread_count,
        },
    })

    return message


@router.patch("/{chat_id}/read")
async def mark_chat_read(
    chat_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(select(Chat).where(Chat.id == chat_id))
    chat = result.scalar_one_or_none()
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    chat.unread_count = 0
    return {"status": "ok"}

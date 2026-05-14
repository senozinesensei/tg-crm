from fastapi import APIRouter, Request
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from app.database import async_session
from app.models.chat import Chat
from app.services.chat_service import get_or_create_contact, get_or_create_chat, create_message
from app.schemas.message import MessageResponse
from app.schemas.chat import ChatResponse
from app.schemas.contact import ContactResponse
from app.websocket.manager import manager
from datetime import datetime

webhook_router = APIRouter()


@webhook_router.post("/webhook/telegram")
async def telegram_webhook(request: Request):
    data = await request.json()

    message = data.get("message")
    if not message:
        return {"ok": True}

    from_user = message.get("from", {})
    text = message.get("text", "")
    telegram_id = from_user.get("id")
    message_id = message.get("message_id")

    if not telegram_id or not text:
        return {"ok": True}

    first_name = from_user.get("first_name")
    last_name = from_user.get("last_name")
    username = from_user.get("username")

    async with async_session() as db:
        try:
            contact, contact_created = await get_or_create_contact(
                db=db,
                telegram_id=telegram_id,
                first_name=first_name,
                last_name=last_name,
                username=username,
            )

            chat, chat_created = await get_or_create_chat(db=db, contact_id=contact.id)

            msg = await create_message(
                db=db,
                chat_id=chat.id,
                text=text,
                direction="incoming",
                telegram_message_id=message_id,
            )

            chat.last_message_text = text
            chat.last_message_at = msg.created_at
            chat.unread_count = (chat.unread_count or 0) + 1

            await db.commit()

            # Broadcast via WebSocket
            msg_data = MessageResponse.model_validate(msg).model_dump(mode="json")

            if chat_created:
                # Reload chat with contact for full response
                result = await db.execute(
                    select(Chat).options(joinedload(Chat.contact)).where(Chat.id == chat.id)
                )
                full_chat = result.scalar_one()
                chat_data = ChatResponse.model_validate(full_chat).model_dump(mode="json")
                await manager.broadcast({"type": "new_chat", "data": chat_data})

            await manager.broadcast({"type": "new_message", "data": msg_data})
            await manager.broadcast({
                "type": "chat_updated",
                "data": {
                    "chat_id": chat.id,
                    "last_message_text": chat.last_message_text,
                    "last_message_at": chat.last_message_at.isoformat() if chat.last_message_at else None,
                    "unread_count": chat.unread_count,
                },
            })

        except Exception as e:
            await db.rollback()
            print(f"Webhook processing error: {e}")
            raise

    return {"ok": True}

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.models.chat import Chat
from app.models.message import Message
from app.models.settings import Settings
from app.schemas.chat import ChatResponse
from app.schemas.message import MessageResponse
from app.services.chat_service import create_message, get_or_create_chat, get_or_create_contact
from app.services.openrouter_service import generate_openrouter_reply
from app.services.telegram_service import send_telegram_message
from app.websocket.manager import manager


class MessageProcessor:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def process_incoming_telegram_message(self, telegram_message: dict) -> None:
        from_user = telegram_message.get("from", {})
        text = telegram_message.get("text", "")
        telegram_id = from_user.get("id")
        message_id = telegram_message.get("message_id")

        if not telegram_id or not text:
            return

        contact, _ = await get_or_create_contact(
            db=self.db,
            telegram_id=telegram_id,
            first_name=from_user.get("first_name"),
            last_name=from_user.get("last_name"),
            username=from_user.get("username"),
        )
        chat, chat_created = await get_or_create_chat(db=self.db, contact_id=contact.id)

        message = await create_message(
            db=self.db,
            chat_id=chat.id,
            text=text,
            direction="incoming",
            telegram_message_id=message_id,
        )

        chat.last_message_text = text
        chat.last_message_at = message.created_at
        chat.unread_count = (chat.unread_count or 0) + 1

        await self.db.commit()
        await self._broadcast_incoming(chat, message, chat_created)
        try:
            await self._send_ai_auto_reply(chat.id)
        except Exception as exc:
            await self.db.rollback()
            print(f"AI auto-reply error: {exc}")

    async def _send_ai_auto_reply(self, chat_id: str) -> None:
        settings = await self._get_settings()
        if not self._ai_enabled(settings):
            return

        chat = await self._get_chat(chat_id)
        if not chat:
            return

        history = await self._get_ai_history(chat_id, settings.openrouter_history_limit)
        ai_text = await generate_openrouter_reply(
            api_key=settings.openrouter_api_key,
            model=settings.openrouter_model,
            system_prompt=settings.openrouter_system_prompt,
            messages=history,
        )
        if not ai_text:
            return

        telegram_response = await send_telegram_message(
            bot_token=settings.bot_token,
            chat_id=chat.contact.telegram_id,
            text=ai_text,
        )
        if not telegram_response:
            print("AI auto-reply generated text, but Telegram send failed")
            return

        message = await create_message(
            db=self.db,
            chat_id=chat.id,
            text=ai_text,
            direction="outgoing",
            telegram_message_id=telegram_response.get("message_id"),
        )
        chat.last_message_text = ai_text
        chat.last_message_at = message.created_at

        await self.db.commit()
        await self._broadcast_message(message)
        await self._broadcast_chat_update(chat)

    async def _broadcast_incoming(self, chat: Chat, message: Message, chat_created: bool) -> None:
        if chat_created:
            full_chat = await self._get_chat(chat.id)
            if full_chat:
                chat_data = ChatResponse.model_validate(full_chat).model_dump(mode="json")
                await manager.broadcast({"type": "new_chat", "data": chat_data})

        await self._broadcast_message(message)
        await self._broadcast_chat_update(chat)

    async def _broadcast_message(self, message: Message) -> None:
        msg_data = MessageResponse.model_validate(message).model_dump(mode="json")
        await manager.broadcast({"type": "new_message", "data": msg_data})

    async def _broadcast_chat_update(self, chat: Chat) -> None:
        await manager.broadcast(
            {
                "type": "chat_updated",
                "data": {
                    "chat_id": chat.id,
                    "last_message_text": chat.last_message_text,
                    "last_message_at": chat.last_message_at.isoformat() if chat.last_message_at else None,
                    "unread_count": chat.unread_count,
                },
            }
        )

    async def _get_settings(self) -> Settings | None:
        result = await self.db.execute(select(Settings).where(Settings.id == 1))
        return result.scalar_one_or_none()

    async def _get_chat(self, chat_id: str) -> Chat | None:
        result = await self.db.execute(
            select(Chat).options(joinedload(Chat.contact)).where(Chat.id == chat_id)
        )
        return result.scalar_one_or_none()

    async def _get_ai_history(self, chat_id: str, limit: int) -> list[dict[str, str]]:
        result = await self.db.execute(
            select(Message)
            .where(Message.chat_id == chat_id)
            .order_by(Message.created_at.desc())
            .limit(limit)
        )
        messages = list(reversed(result.scalars().all()))
        return [
            {
                "role": "user" if message.direction == "incoming" else "assistant",
                "content": message.text,
            }
            for message in messages
        ]

    def _ai_enabled(self, settings: Settings | None) -> bool:
        return bool(
            settings
            and settings.ai_auto_reply_enabled
            and settings.bot_token
            and settings.openrouter_api_key
            and settings.openrouter_model
            and settings.openrouter_system_prompt
            and settings.openrouter_history_limit > 0
        )

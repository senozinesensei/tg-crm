from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.contact import Contact
from app.models.chat import Chat
from app.models.message import Message
from app.models.settings import Settings
from datetime import datetime
from typing import Optional, Tuple
import uuid


async def get_bot_token(db: AsyncSession) -> Optional[str]:
    result = await db.execute(select(Settings).where(Settings.id == 1))
    settings = result.scalar_one_or_none()
    if settings:
        return settings.bot_token
    return None


async def get_or_create_contact(
    db: AsyncSession,
    telegram_id: int,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    username: Optional[str] = None,
) -> Tuple[Contact, bool]:
    result = await db.execute(
        select(Contact).where(Contact.telegram_id == telegram_id)
    )
    contact = result.scalar_one_or_none()
    created = False

    if contact:
        contact.first_name = first_name or contact.first_name
        contact.last_name = last_name or contact.last_name
        contact.username = username or contact.username
        contact.last_activity_at = datetime.utcnow()
    else:
        contact = Contact(
            id=str(uuid.uuid4()),
            telegram_id=telegram_id,
            first_name=first_name,
            last_name=last_name,
            username=username,
            created_at=datetime.utcnow(),
            last_activity_at=datetime.utcnow(),
        )
        db.add(contact)
        await db.flush()
        created = True

    return contact, created


async def get_or_create_chat(db: AsyncSession, contact_id: str) -> Tuple[Chat, bool]:
    result = await db.execute(
        select(Chat).where(Chat.contact_id == contact_id)
    )
    chat = result.scalar_one_or_none()
    created = False

    if not chat:
        chat = Chat(
            id=str(uuid.uuid4()),
            contact_id=contact_id,
            created_at=datetime.utcnow(),
        )
        db.add(chat)
        await db.flush()
        created = True

    return chat, created


async def create_message(
    db: AsyncSession,
    chat_id: str,
    text: str,
    direction: str,
    telegram_message_id: Optional[int] = None,
    sent_by_user_id: Optional[str] = None,
) -> Message:
    message = Message(
        id=str(uuid.uuid4()),
        chat_id=chat_id,
        direction=direction,
        text=text,
        telegram_message_id=telegram_message_id,
        sent_by_user_id=sent_by_user_id,
        created_at=datetime.utcnow(),
    )
    db.add(message)
    await db.flush()
    return message

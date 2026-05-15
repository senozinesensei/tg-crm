from fastapi import APIRouter, Request
from app.database import async_session
from app.services.message_processor import MessageProcessor

webhook_router = APIRouter()


@webhook_router.post("/webhook/telegram")
async def telegram_webhook(request: Request):
    data = await request.json()

    message = data.get("message")
    if not message:
        return {"ok": True}

    async with async_session() as db:
        try:
            processor = MessageProcessor(db)
            await processor.process_incoming_telegram_message(message)
        except Exception as e:
            await db.rollback()
            print(f"Webhook processing error: {e}")
            raise

    return {"ok": True}

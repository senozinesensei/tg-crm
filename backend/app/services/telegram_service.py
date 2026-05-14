import httpx
from typing import Optional


TELEGRAM_API_BASE = "https://api.telegram.org/bot{token}"


async def send_telegram_message(bot_token: str, chat_id: int, text: str) -> Optional[dict]:
    url = f"{TELEGRAM_API_BASE.format(token=bot_token)}/sendMessage"
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json={"chat_id": chat_id, "text": text})
        if response.status_code == 200:
            data = response.json()
            if data.get("ok"):
                return data.get("result")
    return None


async def register_webhook(bot_token: str, webhook_url: str) -> bool:
    url = f"{TELEGRAM_API_BASE.format(token=bot_token)}/setWebhook"
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json={"url": webhook_url})
        if response.status_code == 200:
            data = response.json()
            return data.get("ok", False)
    return False


async def delete_webhook(bot_token: str) -> bool:
    url = f"{TELEGRAM_API_BASE.format(token=bot_token)}/deleteWebhook"
    async with httpx.AsyncClient() as client:
        response = await client.post(url)
        if response.status_code == 200:
            data = response.json()
            return data.get("ok", False)
    return False


async def get_webhook_info(bot_token: str) -> Optional[dict]:
    url = f"{TELEGRAM_API_BASE.format(token=bot_token)}/getWebhookInfo"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code == 200:
            data = response.json()
            if data.get("ok"):
                return data.get("result")
    return None

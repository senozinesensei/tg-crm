from typing import Optional

import httpx


OPENROUTER_CHAT_COMPLETIONS_URL = "https://openrouter.ai/api/v1/chat/completions"


async def generate_openrouter_reply(
    api_key: str,
    model: str,
    system_prompt: str,
    messages: list[dict[str, str]],
) -> Optional[str]:
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            *messages,
        ],
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "X-Title": "Telegram CRM",
    }

    async with httpx.AsyncClient(timeout=45) as client:
        response = await client.post(OPENROUTER_CHAT_COMPLETIONS_URL, json=payload, headers=headers)

    if response.status_code >= 400:
        print(f"OpenRouter error {response.status_code}: {response.text}")
        return None

    data = response.json()
    choices = data.get("choices") or []
    if not choices:
        return None

    content = choices[0].get("message", {}).get("content")
    if not content:
        return None

    return content.strip()

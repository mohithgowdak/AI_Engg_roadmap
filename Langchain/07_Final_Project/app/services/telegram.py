import httpx

from app.config import settings


def to_user_key(chat_id: int | str) -> str:
    return f"tg:{chat_id}"


def parse_inbound_text(payload: dict) -> tuple[str, str] | None:
    message = payload.get("message") or payload.get("edited_message")
    if not message:
        return None

    text = message.get("text")
    chat_id = message.get("chat", {}).get("id")
    if chat_id is None or not text:
        return None
    return to_user_key(chat_id), text


async def send_text_message(chat_id: int | str, message: str) -> dict:
    if not settings.telegram_bot_token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN is not configured")

    url = f"https://api.telegram.org/bot{settings.telegram_bot_token}/sendMessage"
    payload = {
        "chat_id": str(chat_id),
        "text": message,
        "disable_web_page_preview": True,
    }
    async with httpx.AsyncClient(timeout=20) as client:
        response = await client.post(url, json=payload)
        response.raise_for_status()
        return response.json()

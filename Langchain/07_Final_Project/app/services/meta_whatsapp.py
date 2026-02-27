import hashlib
import hmac
import json

import httpx

from app.config import settings


def verify_webhook_token(mode: str, verify_token: str, challenge: str) -> str | None:
    if mode != "subscribe":
        return None
    if verify_token != settings.meta_verify_token:
        return None
    return challenge


def verify_signature(raw_body: bytes, signature_header: str | None) -> bool:
    if not signature_header:
        return False
    try:
        signature = signature_header.split("sha256=")[1]
    except IndexError:
        return False
    digest = hmac.new(
        settings.meta_app_secret.encode("utf-8"), raw_body, hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(digest, signature)


async def send_text_message(to_phone: str, message: str) -> dict:
    url = (
        f"https://graph.facebook.com/{settings.meta_graph_version}/"
        f"{settings.meta_phone_number_id}/messages"
    )
    headers = {
        "Authorization": f"Bearer {settings.meta_access_token}",
        "Content-Type": "application/json",
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to_phone,
        "type": "text",
        "text": {"preview_url": False, "body": message},
    }
    async with httpx.AsyncClient(timeout=20) as client:
        response = await client.post(url, headers=headers, content=json.dumps(payload))
        response.raise_for_status()
        return response.json()

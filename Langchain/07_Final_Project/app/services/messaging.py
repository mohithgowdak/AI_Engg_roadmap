from app.services import meta_whatsapp, telegram

TELEGRAM_PREFIX = "tg:"


def is_telegram_user(user_key: str) -> bool:
    return user_key.startswith(TELEGRAM_PREFIX)


async def send_text_message(user_key: str, message: str) -> dict:
    if is_telegram_user(user_key):
        chat_id = user_key.removeprefix(TELEGRAM_PREFIX)
        return await telegram.send_text_message(chat_id, message)
    return await meta_whatsapp.send_text_message(user_key, message)

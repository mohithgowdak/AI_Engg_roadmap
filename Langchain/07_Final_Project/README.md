# PriceDrop Rebuy MVP (Amazon + Meta WhatsApp/Telegram + Family)

## What is implemented
- Meta WhatsApp Cloud API webhook verification + inbound command handling.
- Telegram bot webhook + inbound command handling.
- Bot commands: `ADD`, `MY`, `FAMILY`, `REMOVE`, `MUTE`.
- Family mapping via chat: `ADD <amazon_link> | <nickname> | <relation_optional> | <quantity>`.
- Amazon link tracking with reference price snapshots.
- Family/member wishlist grouping.
- Celery scheduler for 3-hour checks.
- Alerting for minimum 5% price drop with cooldown support.

## Tech stack
- FastAPI
- PostgreSQL + SQLAlchemy
- Redis + Celery
- Amazon price fetcher using HTTP + BeautifulSoup
- Meta WhatsApp Cloud API
- Telegram Bot API

## Quick setup
1. Copy `.env.example` to `.env` and fill Meta/DB/Redis values.
   - Optional Telegram values: `TELEGRAM_BOT_TOKEN`, `TELEGRAM_WEBHOOK_SECRET`.
2. Install dependencies:
   - `pip install -r requirements.txt`
3. Start API:
   - `uvicorn app.main:app --reload`
4. Start worker:
   - `celery -A app.workers.celery_app.celery_app worker --loglevel=info`
5. Start beat:
   - `celery -A app.workers.celery_app.celery_app beat --loglevel=info`

## Meta Cloud API pre-req checklist
- Create Meta app + WhatsApp product.
- Get `META_ACCESS_TOKEN` and `META_PHONE_NUMBER_ID`.
- Configure webhook endpoint `/webhooks/meta` with verify token.
- Subscribe to WhatsApp message events.
- Add message template for proactive price-drop alerts.

## API notes
- Health: `GET /health`
- Webhook verify: `GET /webhooks/meta`
- Webhook receive: `POST /webhooks/meta`
- Telegram webhook receive: `POST /webhooks/telegram`
- Add item API helper: `POST /watchlist/add`
- Read own wishlist: `GET /watchlist/my/{phone}`
- Read family wishlist: `GET /watchlist/family/{phone}`
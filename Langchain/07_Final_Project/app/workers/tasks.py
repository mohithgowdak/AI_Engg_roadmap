import asyncio
from datetime import datetime

from sqlalchemy import and_, select

from app.database import SessionLocal
from app.models import Alert, FamilyMember, NotificationLog, PriceSnapshot, Product, User, Watchlist
from app.services.alerts import create_alerts_for_snapshot, pending_alerts
from app.services.amazon import fetch_price_from_amazon
from app.services.messaging import send_text_message
from app.workers.celery_app import celery_app


@celery_app.task(name="app.workers.tasks.poll_prices_and_enqueue_alerts")
def poll_prices_and_enqueue_alerts() -> int:
    db = SessionLocal()
    created = 0
    try:
        watchlists = db.execute(
            select(Watchlist, Product)
            .join(Product, Product.id == Watchlist.product_id)
            .where(and_(Watchlist.is_active.is_(True)))
        ).all()
        for watch, product in watchlists:
            try:
                fetched = asyncio.run(fetch_price_from_amazon(product.product_url))
            except Exception:
                continue

            product.last_known_price = fetched.price
            product.updated_at = datetime.utcnow()
            db.add(product)
            snapshot = PriceSnapshot(
                product_id=product.id,
                price=fetched.price,
                in_stock=fetched.in_stock,
                source_url=fetched.product_url,
                confidence=fetched.confidence,
            )
            db.add(snapshot)
            db.commit()
            db.refresh(snapshot)
            alerts = create_alerts_for_snapshot(db, watch, snapshot)
            created += len(alerts)
    finally:
        db.close()
    return created


@celery_app.task(name="app.workers.tasks.send_pending_alerts")
def send_pending_alerts() -> int:
    db = SessionLocal()
    sent = 0
    try:
        alerts = pending_alerts(db)
        for alert in alerts:
            watch = db.get(Watchlist, alert.watchlist_id)
            if not watch:
                continue
            user = db.get(User, alert.user_id)
            if not user:
                continue
            product = db.get(Product, alert.product_id)
            product_name = product.canonical_name if product else "Tracked item"
            product_url = product.product_url if product else None

            if alert.family_member_id:
                member = db.get(FamilyMember, alert.family_member_id)
                member_name = member.nickname if member else "family member"
                relation_text = f" ({member.relation})" if member and member.relation else ""
                message = (
                    f"Family price drop for {member_name}{relation_text}\n"
                    f"{product_name}\n"
                    f"Drop: {alert.drop_pct:.1f}%\n"
                    f"Old: INR {alert.old_price:.2f}\n"
                    f"Now: INR {alert.new_price:.2f}"
                )
            else:
                message = (
                    f"Price dropped {alert.drop_pct:.1f}%\n"
                    f"{product_name}\n"
                    f"Old: INR {alert.old_price:.2f}\n"
                    f"Now: INR {alert.new_price:.2f}"
                )
            if product_url:
                message = f"{message}\n{product_url}"
            try:
                result = asyncio.run(send_text_message(user.phone, message))
                alert.status = "sent"
                alert.sent_at = datetime.utcnow()
                db.add(alert)
                db.add(
                    NotificationLog(
                        alert_id=alert.id,
                        provider_message_id=str(result),
                        payload=message,
                        success=True,
                    )
                )
                sent += 1
            except Exception as exc:
                alert.status = "failed"
                db.add(alert)
                db.add(
                    NotificationLog(
                        alert_id=alert.id, payload=str(exc), success=False, provider_message_id=None
                    )
                )
            db.commit()
    finally:
        db.close()
    return sent

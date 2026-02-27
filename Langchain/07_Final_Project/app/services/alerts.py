from datetime import datetime, timedelta

from sqlalchemy import and_, desc, select
from sqlalchemy.orm import Session

from app.config import settings
from app.models import Alert, FamilyMember, MemberWishlist, PriceSnapshot, Watchlist


def calc_drop_percent(reference_price: float, current_price: float) -> float:
    if reference_price <= 0:
        return 0.0
    return ((reference_price - current_price) / reference_price) * 100


def should_alert(watchlist: Watchlist, current_price: float, now: datetime) -> tuple[bool, float]:
    if watchlist.is_muted or not watchlist.is_active:
        return False, 0.0
    if watchlist.cooldown_until and watchlist.cooldown_until > now:
        return False, 0.0

    drop_pct = calc_drop_percent(watchlist.reference_price, current_price)
    threshold = max(watchlist.min_drop_pct, settings.default_min_drop_percent)
    if watchlist.last_alerted_price is not None:
        incremental_drop = calc_drop_percent(watchlist.last_alerted_price, current_price)
        if incremental_drop < settings.default_min_drop_percent:
            return False, 0.0
    return (drop_pct >= threshold), drop_pct


def create_alerts_for_snapshot(
    db: Session, watchlist: Watchlist, snapshot: PriceSnapshot
) -> list[Alert]:
    now = datetime.utcnow()
    can_alert, drop_pct = should_alert(watchlist, snapshot.price, now)
    if not can_alert or not snapshot.in_stock:
        return []

    duplicate = db.execute(
        select(Alert).where(
            and_(
                Alert.watchlist_id == watchlist.id,
                Alert.new_price == snapshot.price,
                Alert.status.in_(("pending", "sent")),
            )
        )
    ).scalar_one_or_none()
    if duplicate:
        return []

    alerts: list[Alert] = []
    if getattr(watchlist, "quantity", 1) > 0:
        watchlist_alert = Alert(
            watchlist_id=watchlist.id,
            user_id=watchlist.user_id,
            product_id=watchlist.product_id,
            family_member_id=None,
            alert_type="self_price_drop",
            drop_pct=drop_pct,
            old_price=watchlist.reference_price,
            new_price=snapshot.price,
            status="pending",
        )
        alerts.append(watchlist_alert)
        db.add(watchlist_alert)

    member_links = db.execute(
        select(MemberWishlist)
        .where(MemberWishlist.product_id == watchlist.product_id)
        .order_by(desc(MemberWishlist.id))
    ).scalars()
    seen_member_ids: set[int] = set()
    for link in member_links:
        if link.family_member_id in seen_member_ids:
            continue
        seen_member_ids.add(link.family_member_id)

        member = db.get(FamilyMember, link.family_member_id)
        if not member:
            continue
        family_alert = Alert(
            watchlist_id=watchlist.id,
            user_id=watchlist.user_id,
            product_id=watchlist.product_id,
            family_member_id=member.id,
            alert_type="family_gift_drop",
            drop_pct=drop_pct,
            old_price=watchlist.reference_price,
            new_price=snapshot.price,
            status="pending",
        )
        alerts.append(family_alert)
        db.add(family_alert)

    watchlist.last_alerted_price = snapshot.price
    watchlist.cooldown_until = now + timedelta(hours=settings.alert_cooldown_hours)
    db.add(watchlist)
    db.commit()
    return alerts


def pending_alerts(db: Session) -> list[Alert]:
    return list(
        db.execute(
            select(Alert).where(and_(Alert.status == "pending")).order_by(Alert.created_at.asc())
        ).scalars()
    )

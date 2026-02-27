from datetime import datetime
import secrets
import logging

from fastapi import Depends, FastAPI, Header, HTTPException, Query, Request
from fastapi.responses import PlainTextResponse
from sqlalchemy import and_, func, select, text
from sqlalchemy.orm import Session

from app.config import settings
from app.database import Base, engine, get_db
from app.models import (
    Family,
    FamilyMember,
    MemberWishlist,
    NotificationLog,
    PriceSnapshot,
    Product,
    User,
    Watchlist,
)
from app.schemas import AddItemRequest
from app.services.amazon import fetch_price_from_amazon
from app.services.messaging import send_text_message
from app.services.meta_whatsapp import verify_signature, verify_webhook_token
from app.services.telegram import parse_inbound_text


app = FastAPI(title=settings.app_name)
logger = logging.getLogger(__name__)
PENDING_QUANTITY_UPDATES: dict[str, dict[str, str | int]] = {}


def _ensure_runtime_columns() -> None:
    # Lightweight runtime migration for local SQLite/dev environments.
    ddl_statements = [
        "ALTER TABLE watchlists ADD COLUMN quantity INTEGER NOT NULL DEFAULT 1",
        "ALTER TABLE member_wishlist ADD COLUMN quantity INTEGER NOT NULL DEFAULT 1",
    ]
    with engine.begin() as conn:
        for ddl in ddl_statements:
            try:
                conn.execute(text(ddl))
            except Exception:
                # Column probably already exists.
                pass


@app.on_event("startup")
def startup() -> None:
    Base.metadata.create_all(bind=engine)
    _ensure_runtime_columns()


def _get_or_create_user(db: Session, phone: str) -> User:
    user = db.execute(select(User).where(User.phone == phone)).scalar_one_or_none()
    if user:
        return user
    user = User(phone=phone)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def _get_or_create_product(db: Session, source_product_id: str, title: str, url: str, price: float) -> Product:
    product = (
        db.execute(select(Product).where(Product.source_product_id == source_product_id))
        .scalar_one_or_none()
    )
    if product:
        product.canonical_name = title
        product.product_url = url
        product.last_known_price = price
        db.add(product)
        db.commit()
        db.refresh(product)
        return product

    product = Product(
        source="amazon",
        source_product_id=source_product_id,
        canonical_name=title,
        product_url=url,
        last_known_price=price,
        currency="INR",
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def _map_product_to_family_member(
    db: Session, user: User, product_id: int, nickname: str, relation: str | None, quantity: int
) -> str:
    clean_nickname = nickname.strip()
    family = db.execute(select(Family).where(Family.owner_user_id == user.id)).scalar_one_or_none()
    if not family:
        family = Family(name=f"{user.phone} family", owner_user_id=user.id, invite_code=secrets.token_hex(4))
        db.add(family)
        db.commit()
        db.refresh(family)

    member = db.execute(
        select(FamilyMember).where(
            and_(
                FamilyMember.family_id == family.id,
                func.lower(FamilyMember.nickname) == clean_nickname.lower(),
            )
        )
    ).scalar_one_or_none()
    if member:
        if relation and member.relation != relation:
            member.relation = relation
            db.add(member)
            db.commit()
            db.refresh(member)
    else:
        owner_member_exists = db.execute(
            select(FamilyMember).where(
                and_(FamilyMember.family_id == family.id, FamilyMember.user_id == user.id)
            )
        ).scalar_one_or_none()
        member_user_id = user.id
        if owner_member_exists:
            # family_members has unique(family_id, user_id), so we create a
            # synthetic user for additional member nicknames.
            safe_nick = "".join(ch for ch in clean_nickname.lower() if ch.isalnum())[:10] or "member"
            synthetic_phone = f"fm:{user.id}:{safe_nick}"[:32]
            synthetic_user = db.execute(
                select(User).where(User.phone == synthetic_phone)
            ).scalar_one_or_none()
            if not synthetic_user:
                synthetic_user = User(phone=synthetic_phone, name=clean_nickname)
                db.add(synthetic_user)
                db.commit()
                db.refresh(synthetic_user)
            member_user_id = synthetic_user.id

        member = FamilyMember(
            family_id=family.id, user_id=member_user_id, nickname=clean_nickname, relation=relation
        )
        db.add(member)
        db.commit()
        db.refresh(member)

    exists = db.execute(
        select(MemberWishlist).where(
            and_(MemberWishlist.family_member_id == member.id, MemberWishlist.product_id == product_id)
        )
    ).scalar_one_or_none()
    if exists:
        relation_text = f" ({member.relation})" if member.relation else ""
        _start_pending_quantity_update(
            user.phone,
            "member_wishlist",
            exists.id,
            exists.quantity,
            f"{member.nickname}{relation_text}",
        )
        return (
            f"Item already mapped to {member.nickname}{relation_text} (Qty x{exists.quantity}).\n"
            f"Do you want to add more quantity? Reply YES or NO."
        )

    db.add(
        MemberWishlist(
            family_member_id=member.id,
            product_id=product_id,
            added_by_user_id=user.id,
            quantity=quantity,
        )
    )
    db.commit()
    relation_text = f" ({member.relation})" if member.relation else ""
    return f"Mapped to family member: {member.nickname}{relation_text} | Qty x{quantity}."


def _parse_quantity(raw: str | None) -> int:
    if not raw:
        return 1
    try:
        qty = int(raw.strip())
    except (TypeError, ValueError):
        return 1
    return max(1, min(100, qty))


def _try_parse_quantity(raw: str | None) -> int | None:
    if not raw:
        return None
    try:
        qty = int(raw.strip())
    except (TypeError, ValueError):
        return None
    return max(1, min(100, qty))


def _start_pending_quantity_update(
    user_key: str,
    target_type: str,
    target_id: int,
    current_qty: int,
    label: str,
) -> None:
    PENDING_QUANTITY_UPDATES[user_key] = {
        "stage": "confirm",
        "target_type": target_type,
        "target_id": target_id,
        "current_qty": current_qty,
        "label": label,
    }


def _apply_pending_quantity_update(db: Session, pending: dict[str, str | int], delta: int) -> tuple[bool, str]:
    target_type = str(pending["target_type"])
    target_id = int(pending["target_id"])
    label = str(pending["label"])
    if target_type == "watchlist":
        row = db.get(Watchlist, target_id)
        if not row:
            return False, "Could not find that wishlist item anymore."
        row.quantity += delta
        db.add(row)
        db.commit()
        return True, f"Updated quantity for {label}: x{row.quantity}."
    row = db.get(MemberWishlist, target_id)
    if not row:
        return False, "Could not find that family mapping anymore."
    row.quantity += delta
    db.add(row)
    db.commit()
    return True, f"Updated quantity for {label}: x{row.quantity}."


def _parse_add_payload(payload: str) -> tuple[str, str | None, str | None, int]:
    parts = [part.strip() for part in payload.split("|")]
    link = parts[0] if parts else ""
    nickname: str | None = None
    relation: str | None = None
    quantity = 1

    if len(parts) == 2:
        if parts[1].isdigit():
            quantity = _parse_quantity(parts[1])
        elif parts[1]:
            nickname = parts[1]
    elif len(parts) >= 3:
        nickname = parts[1] if parts[1] else None
        if len(parts) >= 4:
            relation = parts[2] if parts[2] else None
            quantity = _parse_quantity(parts[3])
        else:
            if parts[2].isdigit():
                quantity = _parse_quantity(parts[2])
            else:
                relation = parts[2] if parts[2] else None
    return link, nickname, relation, quantity


async def _handle_add(
    db: Session,
    phone: str,
    link: str,
    nickname: str | None = None,
    relation: str | None = None,
    quantity: int = 1,
) -> str:
    user = _get_or_create_user(db, phone)
    try:
        fetched = await fetch_price_from_amazon(link)
    except ValueError:
        return (
            "I could not read that Amazon link.\n"
            "Please send a full product URL like:\n"
            "ADD https://www.amazon.in/dp/B0XXXXXXXX"
        )
    product = _get_or_create_product(
        db, fetched.source_product_id, fetched.title, fetched.product_url, fetched.price
    )

    existing = db.execute(
        select(Watchlist).where(and_(Watchlist.user_id == user.id, Watchlist.product_id == product.id))
    ).scalar_one_or_none()
    if existing:
        mapped_msg = ""
        if nickname:
            mapped_msg = "\n" + _map_product_to_family_member(
                db, user, product.id, nickname, relation, quantity
            )
        else:
            _start_pending_quantity_update(
                user.phone, "watchlist", existing.id, existing.quantity, "your item"
            )
            mapped_msg = (
                f"\nItem already exists in your name (Qty x{existing.quantity}).\n"
                f"Do you want to add more quantity? Reply YES or NO."
            )
        return (
            f"Already tracking this item.\n"
            f"{product.canonical_name}\nCurrent price: INR {fetched.price:.2f}\n"
            f"Quantity: x{existing.quantity}{mapped_msg}"
        )

    watch = Watchlist(
        user_id=user.id,
        product_id=product.id,
        reference_price=fetched.price,
        min_drop_pct=settings.default_min_drop_percent,
        quantity=quantity if not nickname else 0,
    )
    db.add(watch)
    db.add(
        PriceSnapshot(
            product_id=product.id,
            price=fetched.price,
            in_stock=fetched.in_stock,
            source_url=fetched.product_url,
            confidence=fetched.confidence,
        )
    )
    db.commit()
    mapped_msg = ""
    if nickname:
        mapped_msg = "\n" + _map_product_to_family_member(db, user, product.id, nickname, relation, quantity)
    return (
        f"Added to your wishlist.\n"
        f"{product.canonical_name}\n"
        f"Reference price: INR {fetched.price:.2f}\n"
        f"Quantity: x{watch.quantity}\n"
        f"I will check every {settings.default_check_interval_hours} hours and alert at >= {settings.default_min_drop_percent:.0f}% drop."
        f"{mapped_msg}"
    )


def _handle_my(db: Session, phone: str, include_family_mapped: bool = True) -> str:
    user = db.execute(select(User).where(User.phone == phone)).scalar_one_or_none()
    if not user:
        return "No account found yet. Send: ADD <amazon_link>"

    family = db.execute(select(Family).where(Family.owner_user_id == user.id)).scalar_one_or_none()
    mapped_members_by_product: dict[int, list[str]] = {}
    mapped_qty_by_product: dict[int, int] = {}
    if family:
        rows = db.execute(
            select(
                MemberWishlist.product_id,
                FamilyMember.nickname,
                FamilyMember.relation,
                MemberWishlist.quantity,
            )
            .join(FamilyMember, FamilyMember.id == MemberWishlist.family_member_id)
            .where(
                and_(
                    FamilyMember.family_id == family.id,
                    MemberWishlist.added_by_user_id == user.id,
                )
            )
        ).all()
        for product_id, nickname, relation, mapped_quantity in rows:
            relation_text = f" ({relation})" if relation else ""
            label = f"{nickname}{relation_text} x{mapped_quantity}"
            existing = mapped_members_by_product.get(product_id, [])
            if label.lower() not in {item.lower() for item in existing}:
                existing.append(label)
                mapped_members_by_product[product_id] = existing
            mapped_qty_by_product[product_id] = mapped_qty_by_product.get(product_id, 0) + mapped_quantity
    watches = list(
        db.execute(
            select(Watchlist, Product)
            .join(Product, Product.id == Watchlist.product_id)
            .where(and_(Watchlist.user_id == user.id, Watchlist.is_active.is_(True)))
            .order_by(Watchlist.id.asc())
        )
    )
    if not include_family_mapped:
        watches = [(watch, product) for watch, product in watches if watch.quantity > 0]

    if not watches:
        return "Your wishlist is empty. Send: ADD <amazon_link>"

    title = "Your wishlist (all):" if include_family_mapped else "Your wishlist (personal):"
    lines = [title]
    for idx, (watch, product) in enumerate(watches, start=1):
        muted = " (muted)" if watch.is_muted else ""
        mapped_qty = mapped_qty_by_product.get(watch.product_id, 0)
        total_qty = watch.quantity + mapped_qty
        lines.append(
            f"{idx}. [{watch.id}] {product.canonical_name[:60]}{muted} | Ref INR {watch.reference_price:.2f} | Qty x{watch.quantity} | Total x{total_qty}"
        )
        mapped_to = mapped_members_by_product.get(watch.product_id, [])
        recipients: list[str] = []
        if watch.quantity > 0:
            recipients.append(f"You x{watch.quantity}")
        if mapped_to:
            recipients.extend(mapped_to)
        if not recipients:
            recipients = ["Family only"]
        lines.append(f"   Mapped to: {', '.join(recipients)}")
        lines.append(f"   {product.product_url}")
    return "\n".join(lines)


def _handle_family(db: Session, phone: str) -> str:
    user = db.execute(select(User).where(User.phone == phone)).scalar_one_or_none()
    if not user:
        return "No family found. Create one first."

    membership = (
        db.execute(select(FamilyMember).where(FamilyMember.user_id == user.id)).scalar_one_or_none()
    )
    if not membership:
        return "You are not part of a family yet."

    rows = list(
        db.execute(
            select(FamilyMember, MemberWishlist, Product, Watchlist)
            .join(MemberWishlist, MemberWishlist.family_member_id == FamilyMember.id)
            .join(Product, Product.id == MemberWishlist.product_id)
            .outerjoin(
                Watchlist,
                and_(
                    Watchlist.user_id == MemberWishlist.added_by_user_id,
                    Watchlist.product_id == Product.id,
                    Watchlist.is_active.is_(True),
                ),
            )
            .where(FamilyMember.family_id == membership.family_id)
            .order_by(FamilyMember.nickname.asc(), MemberWishlist.id.asc())
        )
    )
    if not rows:
        return "Family wishlist is empty."

    grouped: dict[str, tuple[str, str | None, list[str]]] = {}
    for member, member_wishlist, product, watch in rows:
        key = member.nickname.strip().lower()
        existing = grouped.get(key, (member.nickname, member.relation, []))
        if not existing[1] and member.relation:
            existing = (existing[0], member.relation, existing[2])
        current_price = product.last_known_price if product.last_known_price is not None else 0.0
        details = (
            f"{product.canonical_name[:60]} | Current INR {current_price:.2f} | "
            f"Qty x{member_wishlist.quantity}"
        )
        if watch:
            details = (
                f"[{watch.id}] {details} | Ref INR {watch.reference_price:.2f} | "
                f"Alert >= {watch.min_drop_pct:.0f}%"
            )
        line = f"{details}\n    {product.product_url}"
        if line not in existing[2]:
            existing[2].append(line)
        grouped[key] = existing

    lines = ["Family wishlist:"]
    for _, data in grouped.items():
        nickname, relation, items = data
        relation_text = f" ({relation})" if relation else ""
        lines.append(f"- {nickname}{relation_text}:")
        for i, item in enumerate(items, start=1):
            lines.append(f"  {i}. {item}")
    return "\n".join(lines)


def _handle_remove_or_mute(db: Session, phone: str, cmd: str, watch_id: int) -> str:
    user = db.execute(select(User).where(User.phone == phone)).scalar_one_or_none()
    if not user:
        return "No account found."
    watch = db.execute(
        select(Watchlist).where(and_(Watchlist.id == watch_id, Watchlist.user_id == user.id))
    ).scalar_one_or_none()
    if not watch:
        return "Item not found in your wishlist."

    if cmd == "REMOVE":
        watch.is_active = False
        msg = "Item removed from tracking."
    else:
        watch.is_muted = True
        msg = "Item muted."
    db.add(watch)
    db.commit()
    return msg


def _cleanup_orphan_watchlists(db: Session, user_id: int) -> int:
    family = db.execute(select(Family).where(Family.owner_user_id == user_id)).scalar_one_or_none()
    mapped_by_product: dict[int, int] = {}
    if family:
        rows = db.execute(
            select(MemberWishlist.product_id, MemberWishlist.quantity)
            .join(FamilyMember, FamilyMember.id == MemberWishlist.family_member_id)
            .where(
                and_(
                    FamilyMember.family_id == family.id,
                    MemberWishlist.added_by_user_id == user_id,
                )
            )
        ).all()
        for product_id, qty in rows:
            mapped_by_product[product_id] = mapped_by_product.get(product_id, 0) + int(qty)

    changed = 0
    watches = db.execute(
        select(Watchlist).where(and_(Watchlist.user_id == user_id, Watchlist.is_active.is_(True)))
    ).scalars()
    for watch in watches:
        mapped_qty = mapped_by_product.get(watch.product_id, 0)
        if watch.quantity <= 0 and mapped_qty <= 0:
            watch.is_active = False
            db.add(watch)
            changed += 1
    if changed:
        db.commit()
    return changed


def _handle_remove_all(db: Session, phone: str) -> str:
    user = db.execute(select(User).where(User.phone == phone)).scalar_one_or_none()
    if not user:
        return "No account found."

    deactivated = 0
    watches = db.execute(
        select(Watchlist).where(and_(Watchlist.user_id == user.id, Watchlist.is_active.is_(True)))
    ).scalars()
    for watch in watches:
        watch.is_active = False
        db.add(watch)
        deactivated += 1

    removed_mappings = 0
    family = db.execute(select(Family).where(Family.owner_user_id == user.id)).scalar_one_or_none()
    if family:
        mappings = db.execute(
            select(MemberWishlist)
            .join(FamilyMember, FamilyMember.id == MemberWishlist.family_member_id)
            .where(
                and_(
                    FamilyMember.family_id == family.id,
                    MemberWishlist.added_by_user_id == user.id,
                )
            )
        ).scalars()
        for mapping in mappings:
            db.delete(mapping)
            removed_mappings += 1

    db.commit()
    return (
        f"Removed everything.\n"
        f"- Deactivated watchlist items: {deactivated}\n"
        f"- Removed family mappings: {removed_mappings}"
    )


def _handle_remove_person(db: Session, phone: str, nickname: str) -> str:
    user = db.execute(select(User).where(User.phone == phone)).scalar_one_or_none()
    if not user:
        return "No account found."

    family = db.execute(select(Family).where(Family.owner_user_id == user.id)).scalar_one_or_none()
    if not family:
        return "No family found."

    clean_nickname = nickname.strip().lower()
    members = list(
        db.execute(
            select(FamilyMember).where(
                and_(
                    FamilyMember.family_id == family.id,
                    func.lower(FamilyMember.nickname) == clean_nickname,
                )
            )
        ).scalars()
    )
    if not members:
        return f"No family member found with name '{nickname}'."

    member_ids = [m.id for m in members]
    mappings = list(
        db.execute(
            select(MemberWishlist).where(
                and_(
                    MemberWishlist.family_member_id.in_(member_ids),
                    MemberWishlist.added_by_user_id == user.id,
                )
            )
        ).scalars()
    )
    removed = 0
    for mapping in mappings:
        db.delete(mapping)
        removed += 1
    db.commit()

    cleaned = _cleanup_orphan_watchlists(db, user.id)
    display_name = members[0].nickname
    return (
        f"Removed items mapped to {display_name}.\n"
        f"- Family mappings removed: {removed}\n"
        f"- Orphan watchlist items deactivated: {cleaned}"
    )


async def _dispatch_command(db: Session, phone: str, body: str) -> str:
    text = body.strip()
    upper = text.upper()
    pending = PENDING_QUANTITY_UPDATES.get(phone)
    if pending:
        stage = str(pending["stage"])
        if stage == "confirm":
            if upper in ("NO", "N"):
                PENDING_QUANTITY_UPDATES.pop(phone, None)
                return "Okay, quantity unchanged."
            if upper in ("YES", "Y"):
                pending["stage"] = "amount"
                PENDING_QUANTITY_UPDATES[phone] = pending
                return "How many quantity should I add? Reply with a number (1-100)."
            qty = _try_parse_quantity(text)
            if qty is None:
                return "Please reply YES or NO."
            ok, msg = _apply_pending_quantity_update(db, pending, qty)
            PENDING_QUANTITY_UPDATES.pop(phone, None)
            return msg if ok else f"{msg} Please try ADD again."
        if stage == "amount":
            qty = _try_parse_quantity(text)
            if qty is None:
                return "Please send only a number (1-100)."
            ok, msg = _apply_pending_quantity_update(db, pending, qty)
            PENDING_QUANTITY_UPDATES.pop(phone, None)
            return msg if ok else f"{msg} Please try ADD again."

    if upper.startswith("ADD "):
        link, nickname, relation, quantity = _parse_add_payload(text[4:].strip())
        return await _handle_add(db, phone, link, nickname, relation, quantity)
    if upper == "MY":
        return _handle_my(db, phone, include_family_mapped=False)
    if upper in ("ALL", "MYALL"):
        return _handle_my(db, phone, include_family_mapped=True)
    if upper == "MYPERSONAL":
        # Backward-compatible alias.
        return _handle_my(db, phone, include_family_mapped=False)
    if upper == "FAMILY":
        return _handle_family(db, phone)
    if upper == "REMOVEALL":
        return _handle_remove_all(db, phone)
    if upper.startswith("REMOVEPERSON "):
        return _handle_remove_person(db, phone, text.split(" ", 1)[1])
    if upper.startswith("REMOVEBY "):
        return _handle_remove_person(db, phone, text.split(" ", 1)[1])
    if upper.startswith("REMOVE "):
        return _handle_remove_or_mute(db, phone, "REMOVE", int(text.split(" ")[1]))
    if upper.startswith("MUTE "):
        return _handle_remove_or_mute(db, phone, "MUTE", int(text.split(" ")[1]))

    return (
        "Commands:\n"
        "ADD <amazon_link>\n"
        "ADD <amazon_link> | <quantity>\n"
        "ADD <amazon_link> | <nickname> | <relation_optional> | <quantity>\n"
        "MY\n"
        "ALL\n"
        "FAMILY\n"
        "REMOVEALL\n"
        "REMOVEPERSON <name>\n"
        "REMOVE <watch_id>\n"
        "MUTE <watch_id>"
    )


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/webhooks/meta", response_class=PlainTextResponse)
def verify_meta_webhook(
    mode: str = Query(alias="hub.mode"),
    token: str = Query(alias="hub.verify_token"),
    challenge: str = Query(alias="hub.challenge"),
) -> PlainTextResponse:
    verified = verify_webhook_token(mode=mode, verify_token=token, challenge=challenge)
    if not verified:
        raise HTTPException(status_code=403, detail="Webhook verification failed")
    return PlainTextResponse(content=verified, status_code=200)


@app.post("/webhooks/meta")
async def receive_meta_webhook(
    request: Request,
    x_hub_signature_256: str | None = Header(default=None),
    db: Session = Depends(get_db),
) -> dict[str, bool]:
    raw = await request.body()
    if settings.app_env != "dev" and not verify_signature(raw, x_hub_signature_256):
        raise HTTPException(status_code=401, detail="Invalid signature")

    payload = await request.json()
    entries = payload.get("entry", [])
    for entry in entries:
        for change in entry.get("changes", []):
            value = change.get("value", {})
            messages = value.get("messages", [])
            for message in messages:
                try:
                    from_phone = message.get("from")
                    text_body = message.get("text", {}).get("body", "")
                    if not from_phone or not text_body:
                        continue
                    reply = await _dispatch_command(db, from_phone, text_body)
                    await send_text_message(from_phone, reply)
                except Exception:
                    # Do not fail webhook delivery on outbound send errors.
                    logger.exception("Failed to process incoming WhatsApp message.")
                    continue
    return {"ok": True}


@app.post("/webhooks/telegram")
async def receive_telegram_webhook(
    request: Request,
    x_telegram_bot_api_secret_token: str | None = Header(default=None),
    db: Session = Depends(get_db),
) -> dict[str, bool]:
    if settings.telegram_webhook_secret and (
        x_telegram_bot_api_secret_token != settings.telegram_webhook_secret
    ):
        raise HTTPException(status_code=401, detail="Invalid Telegram webhook secret")

    payload = await request.json()
    parsed = parse_inbound_text(payload)
    if not parsed:
        return {"ok": True}

    from_user, text_body = parsed
    try:
        reply = await _dispatch_command(db, from_user, text_body)
        await send_text_message(from_user, reply)
    except Exception:
        logger.exception("Failed to process incoming Telegram message.")
    return {"ok": True}


@app.post("/watchlist/add")
async def add_watchlist_item(data: AddItemRequest, db: Session = Depends(get_db)) -> dict[str, str]:
    reply = await _handle_add(
        db, data.phone, data.amazon_link, data.nickname, data.relation, data.quantity
    )
    return {"message": reply}


@app.get("/watchlist/my/{phone}")
def my_watchlist(phone: str, db: Session = Depends(get_db)) -> dict[str, str]:
    return {"message": _handle_my(db, phone)}


@app.get("/watchlist/family/{phone}")
def family_watchlist(phone: str, db: Session = Depends(get_db)) -> dict[str, str]:
    return {"message": _handle_family(db, phone)}

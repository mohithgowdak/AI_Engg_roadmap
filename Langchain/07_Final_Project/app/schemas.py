from datetime import datetime

from pydantic import BaseModel, Field


class AddItemRequest(BaseModel):
    phone: str = Field(min_length=8, max_length=32)
    amazon_link: str
    nickname: str | None = None
    relation: str | None = None
    quantity: int = Field(default=1, ge=1, le=100)


class ItemResponse(BaseModel):
    id: int
    product_name: str
    product_url: str
    reference_price: float
    last_known_price: float | None = None
    min_drop_pct: float
    is_muted: bool


class WatchlistResponse(BaseModel):
    phone: str
    items: list[ItemResponse]


class PriceFetchResult(BaseModel):
    source_product_id: str
    title: str
    product_url: str
    price: float
    in_stock: bool = True
    currency: str = "INR"
    confidence: str = "high"


class WebhookInboundMessage(BaseModel):
    from_phone: str
    body: str
    message_id: str | None = None
    timestamp: datetime | None = None


class FamilyWishlistEntry(BaseModel):
    member_name: str
    relation: str | None = None
    items: list[ItemResponse]


class AlertEvent(BaseModel):
    watchlist_id: int
    alert_type: str
    drop_pct: float
    old_price: float
    new_price: float
    message: str

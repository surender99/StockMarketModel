"""Paper orders — ATH-REL-014, REQ-PAPER-ORDERS-001."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from uuid import uuid4


class OrderSide(StrEnum):
    BUY = "buy"
    SELL = "sell"


class OrderStatus(StrEnum):
    PENDING = "pending"
    FILLED = "filled"
    CANCELLED = "cancelled"
    REJECTED = "rejected"


@dataclass
class PaperOrder:
    """Simulated paper order."""

    symbol: str
    side: OrderSide
    quantity: float
    order_id: str = field(default_factory=lambda: uuid4().hex[:12])
    status: OrderStatus = OrderStatus.PENDING
    limit_price: float | None = None
    fill_price: float | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

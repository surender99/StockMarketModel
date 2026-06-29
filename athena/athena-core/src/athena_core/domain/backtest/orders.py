"""Order domain model and state machine — REQ-BT-ORDER-001, ATH-REL-007 §5.2."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from enum import StrEnum
from typing import Literal


class OrderType(StrEnum):
    """Supported order types — FR-002."""

    MARKET = "market"
    LIMIT = "limit"
    STOP = "stop"
    STOP_LIMIT = "stop_limit"


class OrderSide(StrEnum):
    """Order direction."""

    BUY = "buy"
    SELL = "sell"


class OrderStatus(StrEnum):
    """Order lifecycle states."""

    PENDING = "pending"
    SUBMITTED = "submitted"
    PARTIALLY_FILLED = "partially_filled"
    FILLED = "filled"
    CANCELLED = "cancelled"
    REJECTED = "rejected"


_VALID_TRANSITIONS: dict[OrderStatus, frozenset[OrderStatus]] = {
    OrderStatus.PENDING: frozenset({OrderStatus.SUBMITTED, OrderStatus.CANCELLED, OrderStatus.REJECTED}),
    OrderStatus.SUBMITTED: frozenset(
        {OrderStatus.PARTIALLY_FILLED, OrderStatus.FILLED, OrderStatus.CANCELLED, OrderStatus.REJECTED}
    ),
    OrderStatus.PARTIALLY_FILLED: frozenset({OrderStatus.FILLED, OrderStatus.CANCELLED}),
    OrderStatus.FILLED: frozenset(),
    OrderStatus.CANCELLED: frozenset(),
    OrderStatus.REJECTED: frozenset(),
}


@dataclass
class Order:
    """Simulated order — REQ-BT-ORDER-001."""

    order_id: str
    symbol: str
    side: OrderSide
    order_type: OrderType
    quantity: int
    signal_date: date
    limit_price: float | None = None
    stop_price: float | None = None
    status: OrderStatus = OrderStatus.PENDING
    filled_quantity: int = 0
    fill_price: float | None = None
    fill_date: date | None = None
    strategy_id: str = ""
    reason: str = ""

    def transition(self, new_status: OrderStatus) -> None:
        """Advance order state if transition is valid."""
        allowed = _VALID_TRANSITIONS.get(self.status, frozenset())
        if new_status not in allowed:
            msg = f"invalid order transition: {self.status} -> {new_status}"
            raise ValueError(msg)
        self.status = new_status

    def submit(self) -> None:
        self.transition(OrderStatus.SUBMITTED)

    def fill(self, price: float, qty: int, fill_date: date) -> None:
        if self.status not in (OrderStatus.SUBMITTED, OrderStatus.PARTIALLY_FILLED):
            msg = f"cannot fill order in status {self.status}"
            raise ValueError(msg)
        self.filled_quantity += qty
        self.fill_price = price
        self.fill_date = fill_date
        if self.filled_quantity >= self.quantity:
            self.transition(OrderStatus.FILLED)
        else:
            self.status = OrderStatus.PARTIALLY_FILLED


def validate_order(order: Order) -> list[str]:
    """Return validation errors for an order."""
    errors: list[str] = []
    if order.quantity <= 0:
        errors.append("quantity must be positive")
    if order.order_type in (OrderType.LIMIT, OrderType.STOP_LIMIT) and order.limit_price is None:
        errors.append("limit orders require limit_price")
    if order.order_type in (OrderType.STOP, OrderType.STOP_LIMIT) and order.stop_price is None:
        errors.append("stop orders require stop_price")
    return errors


@dataclass
class PendingEntry:
    """Queued entry awaiting next-bar execution — REQ-BT-EXECUTION-001."""

    symbol: str
    signal_date: date
    side: Literal["long"] = "long"
    strategy_id: str = ""
    reason: str = field(default="")

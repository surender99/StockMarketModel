"""Open position model — REQ-PF-001."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Literal


@dataclass
class OpenPosition:
    """Active position during simulation or live portfolio."""

    symbol: str
    side: Literal["long"]
    entry_date: date
    entry_price: float
    quantity: int
    entry_fees: float
    stop_price: float | None = None
    target_price: float | None = None

    def market_value(self, mark: float) -> float:
        return self.quantity * mark

    def unrealized_pnl(self, mark: float) -> float:
        return (mark - self.entry_price) * self.quantity

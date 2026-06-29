"""Paper positions — ATH-REL-014, REQ-PAPER-POSITIONS-001."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class PaperPosition:
    """Open paper position."""

    symbol: str
    quantity: float
    avg_price: float

    @property
    def market_value(self) -> float:
        return self.quantity * self.avg_price

    def update(self, quantity_delta: float, price: float) -> None:
        if self.quantity + quantity_delta == 0:
            self.quantity = 0
            self.avg_price = 0.0
            return
        total_cost = self.avg_price * self.quantity + price * quantity_delta
        self.quantity += quantity_delta
        self.avg_price = total_cost / self.quantity if self.quantity else 0.0

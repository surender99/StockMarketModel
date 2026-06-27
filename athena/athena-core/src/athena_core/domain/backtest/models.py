"""Backtest domain models — REQ-BT-ENGINE-001."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Literal


@dataclass(frozen=True)
class TradeRecord:
    """Completed round-trip trade."""

    symbol: str
    side: Literal["long"]
    entry_date: date
    exit_date: date
    entry_price: float
    exit_price: float
    quantity: int
    entry_fees: float
    exit_fees: float
    gross_pnl: float
    net_pnl: float
    exit_reason: str


@dataclass
class OpenPosition:
    """Active position during simulation."""

    symbol: str
    side: Literal["long"]
    entry_date: date
    entry_price: float
    quantity: int
    entry_fees: float
    stop_price: float | None = None
    target_price: float | None = None


@dataclass
class PortfolioState:
    """Mutable portfolio snapshot."""

    cash: float
    positions: dict[str, OpenPosition] = field(default_factory=dict)

    def position_count(self) -> int:
        return len(self.positions)

    def equity(self, marks: dict[str, float]) -> float:
        mtm = sum(
            pos.quantity * marks.get(sym, pos.entry_price) for sym, pos in self.positions.items()
        )
        return self.cash + mtm

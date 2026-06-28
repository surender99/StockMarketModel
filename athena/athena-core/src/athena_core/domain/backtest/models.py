"""Backtest domain models — REQ-BT-ENGINE-001."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Literal

from athena_core.domain.portfolio import OpenPosition, PortfolioState

__all__ = ["OpenPosition", "PortfolioState", "TradeRecord"]


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

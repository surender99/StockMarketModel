"""In-memory tick store — ATH-IP-000011 Tick-Repository MVP."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass(frozen=True, slots=True)
class Tick:
    symbol: str
    price: Decimal
    size: Decimal
    ts: datetime


class TickRepository:
    """Append-only tick buffer with symbol-scoped reads."""

    def __init__(self) -> None:
        self._ticks: list[Tick] = []

    def append(self, tick: Tick) -> None:
        self._ticks.append(tick)

    def latest(self, symbol: str, limit: int = 100) -> list[Tick]:
        matched = [t for t in self._ticks if t.symbol == symbol]
        return matched[-limit:]

    def clear(self) -> None:
        self._ticks.clear()

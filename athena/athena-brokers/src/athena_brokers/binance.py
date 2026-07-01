"""Binance broker stub."""

from __future__ import annotations

from typing import Any


class BinanceBroker:
    broker_id = "binance"

    def connect(self, credentials: dict[str, str]) -> None:
        _ = credentials

    def place_order(self, order: dict[str, Any]) -> str:
        return f"binance-order-{order.get('symbol', 'UNKNOWN')}"

    def disconnect(self) -> None:
        return None


__all__ = ["BinanceBroker"]

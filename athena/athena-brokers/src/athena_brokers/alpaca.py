"""Alpaca broker stub."""

from __future__ import annotations

from typing import Any


class AlpacaBroker:
    broker_id = "alpaca"

    def connect(self, credentials: dict[str, str]) -> None:
        _ = credentials

    def place_order(self, order: dict[str, Any]) -> str:
        return f"alpaca-order-{order.get('symbol', 'UNKNOWN')}"

    def disconnect(self) -> None:
        return None


__all__ = ["AlpacaBroker"]

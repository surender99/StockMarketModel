"""Zerodha broker stub."""

from __future__ import annotations

from typing import Any


class ZerodhaBroker:
    broker_id = "zerodha"

    def connect(self, credentials: dict[str, str]) -> None:
        _ = credentials

    def place_order(self, order: dict[str, Any]) -> str:
        return f"zerodha-order-{order.get('symbol', 'UNKNOWN')}"

    def disconnect(self) -> None:
        return None


__all__ = ["ZerodhaBroker"]

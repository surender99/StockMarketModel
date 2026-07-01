"""Tick size rules stub."""

from __future__ import annotations


def tick_size_for_price(price: float, exchange: str = "NSE") -> float:
    if exchange == "NSE":
        return 0.05 if price < 250 else 0.10
    return 0.01


__all__ = ["tick_size_for_price"]

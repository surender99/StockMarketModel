"""Lot size rules stub."""

from __future__ import annotations


def lot_size_for_symbol(symbol: str, exchange: str = "NSE") -> int:
    _ = exchange
    return 1 if symbol else 1


__all__ = ["lot_size_for_symbol"]

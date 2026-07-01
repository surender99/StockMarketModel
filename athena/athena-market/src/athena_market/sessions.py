"""Trading session metadata stub."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class TradingSession:
    exchange: str
    open_time: str
    close_time: str


NSE_SESSION = TradingSession(exchange="NSE", open_time="09:15", close_time="15:30")

__all__ = ["NSE_SESSION", "TradingSession"]

"""Trading calendar port — REQ-DATA-CALENDAR-001."""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import date


class TradingCalendarPort(ABC):
    """Injectable NSE trading calendar interface."""

    @abstractmethod
    def is_trading_day(self, d: date) -> bool:
        """Return True if *d* is an NSE trading session."""

    @abstractmethod
    def trading_days_between(self, start: date, end: date) -> list[date]:
        """Return trading days in [start, end] inclusive."""

    @abstractmethod
    def next_trading_day(self, d: date) -> date:
        """Return the next trading day strictly after *d*."""

    @abstractmethod
    def previous_trading_day(self, d: date) -> date:
        """Return the previous trading day strictly before *d*."""

    @abstractmethod
    def holidays_for_year(self, year: int) -> list[date]:
        """Return configured holidays for *year*."""

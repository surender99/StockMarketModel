"""NSE trading calendar adapter — REQ-DATA-CALENDAR-001."""

from __future__ import annotations

from datetime import date, timedelta
from pathlib import Path

import yaml

from athena_core.domain.ports.trading_calendar import TradingCalendarPort

_DEFAULT_HOLIDAYS = Path(__file__).resolve().parents[3] / "config" / "nse_holidays.yaml"
_MAX_NAV_STEPS = 10
_WEEKEND = {5, 6}  # Saturday, Sunday


class NSETradingCalendar(TradingCalendarPort):
    """Static YAML-backed NSE calendar."""

    def __init__(
        self,
        holidays_file: Path | str | None = None,
        weekend_days: tuple[int, ...] = (5, 6),
    ) -> None:
        path = Path(holidays_file) if holidays_file else _DEFAULT_HOLIDAYS
        self._weekend = set(weekend_days)
        self._holidays = self._load_holidays(path)

    @staticmethod
    def _load_holidays(path: Path) -> set[date]:
        with path.open(encoding="utf-8") as fh:
            raw = yaml.safe_load(fh)
        entries = raw.get("holidays", []) if isinstance(raw, dict) else raw
        return {date.fromisoformat(str(item)) for item in entries}

    def is_trading_day(self, d: date) -> bool:
        if d.weekday() in self._weekend:
            return False
        return d not in self._holidays

    def trading_days_between(self, start: date, end: date) -> list[date]:
        if start > end:
            return []
        days: list[date] = []
        current = start
        while current <= end:
            if self.is_trading_day(current):
                days.append(current)
            current += timedelta(days=1)
        return days

    def next_trading_day(self, d: date) -> date:
        candidate = d + timedelta(days=1)
        for _ in range(_MAX_NAV_STEPS):
            if self.is_trading_day(candidate):
                return candidate
            candidate += timedelta(days=1)
        msg = f"No trading day within {_MAX_NAV_STEPS} steps after {d}"
        raise ValueError(msg)

    def previous_trading_day(self, d: date) -> date:
        candidate = d - timedelta(days=1)
        for _ in range(_MAX_NAV_STEPS):
            if self.is_trading_day(candidate):
                return candidate
            candidate -= timedelta(days=1)
        msg = f"No trading day within {_MAX_NAV_STEPS} steps before {d}"
        raise ValueError(msg)

    def holidays_for_year(self, year: int) -> list[date]:
        return sorted(h for h in self._holidays if h.year == year)

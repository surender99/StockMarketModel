"""Tests for NSE trading calendar — REQ-DATA-CALENDAR-001."""

from __future__ import annotations

from datetime import date
from pathlib import Path

import pytest
import yaml

from athena_core.domain.ports.trading_calendar import TradingCalendarPort
from athena_core.infrastructure.nse_calendar import NSETradingCalendar


@pytest.fixture
def calendar() -> NSETradingCalendar:
    return NSETradingCalendar()


@pytest.fixture
def empty_holiday_calendar(tmp_path: Path) -> NSETradingCalendar:
    path = tmp_path / "empty.yaml"
    path.write_text(yaml.dump({"holidays": []}), encoding="utf-8")
    return NSETradingCalendar(holidays_file=path)


def test_port_is_abstract() -> None:
    assert issubclass(NSETradingCalendar, TradingCalendarPort)


def test_weekend_rejection(calendar: NSETradingCalendar) -> None:
    assert calendar.is_trading_day(date(2024, 1, 6)) is False  # Saturday
    assert calendar.is_trading_day(date(2024, 1, 7)) is False  # Sunday


@pytest.mark.parametrize(
    ("holiday", "label"),
    [
        (date(2024, 1, 26), "Republic Day 2024"),
        (date(2024, 3, 25), "Holi 2024"),
        (date(2024, 8, 15), "Independence Day 2024"),
        (date(2024, 11, 1), "Diwali 2024"),
        (date(2024, 12, 25), "Christmas 2024"),
        (date(2025, 1, 26), "Republic Day 2025"),
        (date(2025, 3, 14), "Holi 2025"),
        (date(2025, 8, 15), "Independence Day 2025"),
        (date(2025, 10, 21), "Diwali 2025"),
        (date(2025, 12, 25), "Christmas 2025"),
    ],
)
def test_known_holidays(calendar: NSETradingCalendar, holiday: date, label: str) -> None:
    assert calendar.is_trading_day(holiday) is False, label


def test_trading_day_after_holiday(calendar: NSETradingCalendar) -> None:
    assert calendar.is_trading_day(date(2024, 1, 29)) is True


def test_trading_days_between_excludes_weekends_and_holidays(calendar: NSETradingCalendar) -> None:
    days = calendar.trading_days_between(date(2024, 1, 24), date(2024, 1, 30))
    assert date(2024, 1, 26) not in days
    assert date(2024, 1, 27) not in days
    assert date(2024, 1, 29) in days


def test_next_and_previous_trading_day(calendar: NSETradingCalendar) -> None:
    assert calendar.next_trading_day(date(2024, 1, 26)) == date(2024, 1, 29)
    assert calendar.previous_trading_day(date(2024, 1, 26)) == date(2024, 1, 25)


def test_empty_holiday_file_weekends_only(empty_holiday_calendar: NSETradingCalendar) -> None:
    cal = empty_holiday_calendar
    assert cal.is_trading_day(date(2024, 1, 2)) is True
    assert cal.is_trading_day(date(2024, 1, 6)) is False


def test_holidays_for_year(calendar: NSETradingCalendar) -> None:
    holidays_2024 = calendar.holidays_for_year(2024)
    assert date(2024, 1, 26) in holidays_2024
    assert all(h.year == 2024 for h in holidays_2024)


def test_mock_injectable_calendar(tmp_path: Path) -> None:
    path = tmp_path / "mock.yaml"
    path.write_text(yaml.dump({"holidays": ["2024-06-01"]}), encoding="utf-8")
    cal = NSETradingCalendar(holidays_file=path)
    assert cal.is_trading_day(date(2024, 6, 1)) is False

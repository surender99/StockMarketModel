"""Date and time helpers — ATH-REL-001 §07-Core-Utilities."""

from __future__ import annotations

from datetime import date, datetime, timezone


def utc_now() -> datetime:
    """Return timezone-aware UTC timestamp."""
    return datetime.now(tz=timezone.utc)


def ensure_date(value: date | datetime | str) -> date:
    """Normalize supported inputs to a calendar date."""
    if isinstance(value, date) and not isinstance(value, datetime):
        return value
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, str):
        return date.fromisoformat(value)
    msg = f"unsupported date value: {value!r}"
    raise TypeError(msg)

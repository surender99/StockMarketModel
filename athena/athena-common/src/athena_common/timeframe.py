"""Shared timeframe enumeration."""

from __future__ import annotations

from enum import StrEnum


class TimeFrame(StrEnum):
    """Bar aggregation timeframe."""

    M1 = "1m"
    M5 = "5m"
    M15 = "15m"
    M30 = "30m"
    H1 = "1h"
    H4 = "4h"
    D1 = "1d"
    W1 = "1w"
    MN1 = "1M"

    @property
    def is_intraday(self) -> bool:
        return self in {TimeFrame.M1, TimeFrame.M5, TimeFrame.M15, TimeFrame.M30, TimeFrame.H1, TimeFrame.H4}

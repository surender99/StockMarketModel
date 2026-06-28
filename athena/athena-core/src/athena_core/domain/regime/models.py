"""Regime classification types — REQ-REGIME-001."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from enum import StrEnum


class TrendRegime(StrEnum):
    """Directional market trend label."""

    BULL = "bull"
    BEAR = "bear"
    SIDEWAYS = "sideways"


class VolatilityRegime(StrEnum):
    """Volatility level label."""

    HIGH = "high"
    LOW = "low"


@dataclass(frozen=True)
class RegimeState:
    """Regime snapshot for a single as-of date — REQ-REGIME-001."""

    as_of: date
    trend: TrendRegime
    volatility: VolatilityRegime
    adx: float
    atr_pct: float
    rolling_vol: float
    nifty_trend: TrendRegime | None = None

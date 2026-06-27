"""Regime engine configuration — REQ-REGIME-001."""

from __future__ import annotations

from pydantic import BaseModel, Field


class RegimeConfig(BaseModel):
    """Thresholds and periods for regime classification — REQ-REGIME-001."""

    benchmark_symbol: str = "^NSEI"
    ema_fast_period: int = Field(default=50, ge=2)
    ema_slow_period: int = Field(default=200, ge=2)
    adx_period: int = Field(default=14, ge=2)
    adx_sideways_threshold: float = Field(default=20.0, ge=0)
    atr_period: int = Field(default=14, ge=2)
    rolling_vol_window: int = Field(default=20, ge=2)
    vol_high_percentile: float = Field(default=0.75, ge=0, le=1)
    vol_lookback_days: int = Field(default=252, ge=20)

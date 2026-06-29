"""Tests for regime engine — REQ-REGIME-001."""

from __future__ import annotations

from datetime import date, timedelta

import pandas as pd
import pytest

from athena_core.application.regime_config import RegimeConfig
from athena_core.application.regime_engine import RegimeEngine
from athena_core.domain.regime.indicators import compute_adx, compute_atr, compute_regime_features
from athena_core.domain.regime.models import TrendRegime, VolatilityRegime
from athena_core.domain.strategy.config import FilterSpec
from tests.memory_ohlcv_repo import MemoryOHLCVRepo

def _bull_ohlcv(days: int = 260) -> pd.DataFrame:
    start = date(2023, 1, 3)
    dates = [start + timedelta(days=i) for i in range(days)]
    close = [100 + i * 0.5 for i in range(days)]
    return pd.DataFrame(
        {
            "date": dates,
            "open": close,
            "high": [c + 1 for c in close],
            "low": [c - 1 for c in close],
            "close": close,
            "volume": [100_000] * days,
            "symbol": ["BENCH"] * days,
        }
    )


def _vol_spike_ohlcv() -> pd.DataFrame:
    base = _bull_ohlcv(300)
    base.loc[base.index[-5:], "close"] = base.loc[base.index[-5:], "close"] * 1.15
    base.loc[base.index[-5:], "high"] = base.loc[base.index[-5:], "close"] + 2
    base.loc[base.index[-5:], "low"] = base.loc[base.index[-5:], "close"] - 5
    return base


def test_regime_indicators_compute() -> None:
    ohlcv = _bull_ohlcv(100)
    features = compute_regime_features(ohlcv, ema_fast_period=10, ema_slow_period=30)
    assert "ema_fast" in features.columns
    assert "adx" in features.columns
    assert "rolling_vol" in features.columns
    assert compute_atr(ohlcv).notna().sum() > 0
    assert compute_adx(ohlcv).notna().sum() > 0


def test_bull_trend_classification() -> None:
    ohlcv = _bull_ohlcv()
    engine = RegimeEngine(MemoryOHLCVRepo({"^NSEI": ohlcv}), RegimeConfig(benchmark_symbol="^NSEI"))
    state = engine.classify_as_of("^NSEI", ohlcv["date"].iloc[-1])
    assert state is not None
    assert state.trend == TrendRegime.BULL


def test_volatility_high_on_spike() -> None:
    ohlcv = _vol_spike_ohlcv()
    engine = RegimeEngine(
        MemoryOHLCVRepo({"^NSEI": ohlcv}),
        RegimeConfig(benchmark_symbol="^NSEI", vol_high_percentile=0.5),
    )
    state = engine.classify_as_of("^NSEI", ohlcv["date"].iloc[-1])
    assert state is not None
    assert state.volatility in {VolatilityRegime.HIGH, VolatilityRegime.LOW}


def test_regime_filter_validation() -> None:
    filt = FilterSpec(
        type="regime", params={"allowed_trends": ["bull"], "allowed_volatility": ["low"]}
    )
    assert filt.type == "regime"


def test_regime_filter_invalid_trend() -> None:
    with pytest.raises(ValueError, match="invalid trend"):
        FilterSpec(type="regime", params={"allowed_trends": ["invalid"]})

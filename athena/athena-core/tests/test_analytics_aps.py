"""Analytics APS tests — PHASE-8 QARIP."""

from __future__ import annotations

import numpy as np
import pandas as pd

from datetime import date

from athena_core.domain.analytics import (
    ANALYTICS_CATALOG,
    AnalyticsPipeline,
    analyze_risk,
    list_mvp_analytics,
    lookup_analytics_aps,
)
from athena_core.domain.backtest import TradeRecord


def _equity_curve(n: int = 100) -> pd.DataFrame:
    dates = pd.date_range("2020-01-01", periods=n, freq="B")
    equity = 100_000 + np.cumsum(np.random.default_rng(42).normal(50, 200, n))
    return pd.DataFrame({"date": dates, "equity": equity})


def test_analytics_catalog_covers_160_aps() -> None:
    assert len(ANALYTICS_CATALOG) == 160
    assert len(list_mvp_analytics()) >= 15


def test_lookup_analytics_aps() -> None:
    entry = lookup_analytics_aps("APS-RISK-DRAWDOWN-001")
    assert entry is not None
    assert entry.domain == "Risk-Intelligence"
    assert entry.status == "MVP"


def test_analyze_risk_returns_metrics() -> None:
    report = analyze_risk(_equity_curve())
    assert report.metrics.max_drawdown <= 0
    assert report.metrics.volatility >= 0


def test_analytics_pipeline_produces_report() -> None:
    equity = _equity_curve()
    trades = [
        TradeRecord(
            symbol="TEST",
            side="long",
            entry_date=date(2020, 1, 15),
            exit_date=date(2020, 1, 25),
            entry_price=100.0,
            exit_price=105.0,
            quantity=10,
            entry_fees=1.0,
            exit_fees=1.0,
            gross_pnl=50.0,
            net_pnl=48.0,
            exit_reason="signal",
        )
    ]
    pipeline = AnalyticsPipeline()
    report = pipeline.run(equity, trades, initial_capital=100_000.0)
    assert report.performance is not None
    assert report.risk is not None
    assert len(report.stages) == len(pipeline.stages)

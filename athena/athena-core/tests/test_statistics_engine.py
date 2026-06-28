"""Statistics engine tests — REQ-STAT-001, REQ-STAT-002."""

from __future__ import annotations

from datetime import date, timedelta

import pandas as pd

from athena_core.application.statistics_engine import StatisticsEngine
from athena_core.domain.backtest import TradeRecord


def _equity_curve(n: int = 60, start: float = 100_000.0, drift: float = 0.001) -> pd.DataFrame:
    dates = [date(2024, 1, 2) + timedelta(days=i) for i in range(n)]
    equity = [start * (1 + drift) ** i for i in range(n)]
    return pd.DataFrame({"date": dates, "equity": equity, "cash": [0.0] * n})


def _trades() -> list[TradeRecord]:
    return [
        TradeRecord(
            symbol="A",
            side="long",
            entry_date=date(2024, 1, 2),
            exit_date=date(2024, 1, 10),
            entry_price=100.0,
            exit_price=110.0,
            quantity=10,
            entry_fees=1.0,
            exit_fees=1.0,
            gross_pnl=100.0,
            net_pnl=98.0,
            exit_reason="signal",
        ),
        TradeRecord(
            symbol="B",
            side="long",
            entry_date=date(2024, 1, 5),
            exit_date=date(2024, 1, 12),
            entry_price=50.0,
            exit_price=45.0,
            quantity=20,
            entry_fees=1.0,
            exit_fees=1.0,
            gross_pnl=-100.0,
            net_pnl=-102.0,
            exit_reason="stop_loss",
        ),
    ]


def test_performance_metrics_req_stat_001() -> None:
    engine = StatisticsEngine()
    stats = engine.compute_performance(_equity_curve(), _trades(), initial_capital=100_000.0)
    assert stats.trade_count == 2
    assert stats.win_rate == 0.5
    assert stats.profit_factor is not None and stats.profit_factor > 0
    assert stats.expectancy is not None
    assert stats.max_drawdown <= 0
    assert stats.sharpe is not None


def test_bootstrap_sharpe_req_stat_002() -> None:
    engine = StatisticsEngine()
    result = engine.bootstrap_sharpe(_equity_curve(), n_samples=200, seed=7)
    assert result.sample_count == 200
    assert result.lower_bound <= result.point_estimate <= result.upper_bound


def test_monte_carlo_req_stat_003() -> None:
    engine = StatisticsEngine()
    result = engine.monte_carlo_returns(_equity_curve(), n_simulations=300, seed=11)
    assert result.simulations == 300
    assert result.percentile_5 <= result.median_return <= result.percentile_95
    assert 0.0 <= result.prob_positive <= 1.0
    assert 0.0 <= result.stability_score <= 1.0


def test_statistics_report_dict() -> None:
    engine = StatisticsEngine()
    stats = engine.compute_performance(_equity_curve(), _trades(), initial_capital=100_000.0)
    bootstrap = engine.bootstrap_sharpe(_equity_curve(), n_samples=50, seed=1)
    monte = engine.monte_carlo_returns(_equity_curve(), n_simulations=50, seed=2)
    report = engine.to_report_dict(stats, bootstrap, monte)
    assert "expectancy" in report
    assert "bootstrap_sharpe" in report
    assert "monte_carlo" in report

"""Statistics engine — AES-1100, REQ-STAT-001, REQ-STAT-002."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any

import numpy as np
import pandas as pd

from athena_core.application.backtest_metrics import compute_metrics
from athena_core.domain.backtest import TradeRecord


@dataclass(frozen=True)
class PerformanceStatistics:
    """Core performance metrics — REQ-STAT-001."""

    total_return: float
    cagr: float
    max_drawdown: float
    sharpe: float | None
    win_rate: float | None
    profit_factor: float | None
    expectancy: float | None
    trade_count: int


@dataclass(frozen=True)
class BootstrapResult:
    """Bootstrap confidence interval for a metric — REQ-STAT-002."""

    metric_name: str
    point_estimate: float
    lower_bound: float
    upper_bound: float
    sample_count: int


class StatisticsEngine:
    """Compute and validate strategy performance statistics."""

    def compute_performance(
        self,
        equity_curve: pd.DataFrame,
        trades: list[TradeRecord],
        *,
        initial_capital: float,
        trading_days_per_year: int = 252,
    ) -> PerformanceStatistics:
        """Derive core metrics from equity curve and trades — REQ-STAT-001."""
        raw = compute_metrics(
            equity_curve,
            trades,
            initial_capital=initial_capital,
            trading_days_per_year=trading_days_per_year,
        )
        expectancy = self._expectancy(trades)
        trade_count = raw["trade_count"]
        return PerformanceStatistics(
            total_return=float(raw["total_return"] or 0.0),
            cagr=float(raw["cagr"] or 0.0),
            max_drawdown=float(raw["max_drawdown"] or 0.0),
            sharpe=raw["sharpe"] if isinstance(raw["sharpe"], (int, float)) else None,
            win_rate=raw["win_rate"] if isinstance(raw["win_rate"], (int, float)) else None,
            profit_factor=raw["profit_factor"]
            if isinstance(raw["profit_factor"], (int, float))
            else None,
            expectancy=expectancy,
            trade_count=int(trade_count) if isinstance(trade_count, int) else 0,
        )

    @staticmethod
    def _expectancy(trades: list[TradeRecord]) -> float | None:
        if not trades:
            return None
        return float(sum(t.net_pnl for t in trades) / len(trades))

    def bootstrap_sharpe(
        self,
        equity_curve: pd.DataFrame,
        *,
        n_samples: int = 500,
        confidence: float = 0.95,
        seed: int = 42,
        trading_days_per_year: int = 252,
    ) -> BootstrapResult:
        """Bootstrap daily returns to estimate Sharpe confidence interval — REQ-STAT-002."""
        if equity_curve.empty or len(equity_curve) < 3:
            return BootstrapResult(
                metric_name="sharpe",
                point_estimate=0.0,
                lower_bound=0.0,
                upper_bound=0.0,
                sample_count=0,
            )

        equity = equity_curve["equity"].astype(float)
        daily_returns = equity.pct_change().dropna().to_numpy()
        rng = np.random.default_rng(seed)
        sharpes: list[float] = []
        n = len(daily_returns)
        for _ in range(n_samples):
            sample = rng.choice(daily_returns, size=n, replace=True)
            std = float(sample.std())
            if std > 0:
                sharpes.append(float((sample.mean() / std) * math.sqrt(trading_days_per_year)))

        if not sharpes:
            point = 0.0
            lo, hi = 0.0, 0.0
        else:
            arr = np.array(sharpes)
            point = float(arr.mean())
            alpha = (1.0 - confidence) / 2.0
            lo = float(np.quantile(arr, alpha))
            hi = float(np.quantile(arr, 1.0 - alpha))

        return BootstrapResult(
            metric_name="sharpe",
            point_estimate=point,
            lower_bound=lo,
            upper_bound=hi,
            sample_count=n_samples,
        )

    def to_report_dict(
        self, stats: PerformanceStatistics, bootstrap: BootstrapResult | None = None
    ) -> dict[str, Any]:
        """Serialize statistics for experiment compare / backtest reports."""
        payload: dict[str, Any] = {
            "total_return": stats.total_return,
            "cagr": stats.cagr,
            "max_drawdown": stats.max_drawdown,
            "sharpe": stats.sharpe,
            "win_rate": stats.win_rate,
            "profit_factor": stats.profit_factor,
            "expectancy": stats.expectancy,
            "trade_count": stats.trade_count,
        }
        if bootstrap is not None:
            payload["bootstrap_sharpe"] = {
                "point_estimate": bootstrap.point_estimate,
                "lower_bound": bootstrap.lower_bound,
                "upper_bound": bootstrap.upper_bound,
                "sample_count": bootstrap.sample_count,
            }
        return payload

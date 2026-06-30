"""Risk intelligence facade — PHASE 8 QARIP."""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from athena_core.domain.statistics.risk_metrics import RiskMetrics, compute_risk_metrics


@dataclass(frozen=True, slots=True)
class RiskReport:
    """Consolidated risk analytics output — APS-RISK-DRAWDOWN-001, APS-REPORT-RISK-001."""

    metrics: RiskMetrics
    sortino: float | None = None


def analyze_risk(
    equity_curve: pd.DataFrame,
    *,
    trading_days_per_year: int = 252,
    var_confidence: float = 0.95,
    risk_free_rate: float = 0.0,
) -> RiskReport:
    """Run risk intelligence pipeline on an equity curve."""
    metrics = compute_risk_metrics(
        equity_curve,
        trading_days_per_year=trading_days_per_year,
        var_confidence=var_confidence,
    )
    sortino = _sortino_from_equity(
        equity_curve,
        trading_days_per_year=trading_days_per_year,
        risk_free_rate=risk_free_rate,
    )
    return RiskReport(metrics=metrics, sortino=sortino)


def _sortino_from_equity(
    equity_curve: pd.DataFrame,
    *,
    trading_days_per_year: int,
    risk_free_rate: float,
) -> float | None:
    if equity_curve.empty or "equity" not in equity_curve.columns:
        return None
    returns = equity_curve["equity"].astype(float).pct_change().dropna()
    if len(returns) < 2:
        return None
    daily_rf = risk_free_rate / trading_days_per_year
    excess = returns - daily_rf
    downside = excess[excess < 0]
    if len(downside) == 0:
        return None
    downside_dev = float(downside.std(ddof=1))
    if downside_dev == 0:
        return None
    mean_excess = float(excess.mean())
    return mean_excess / downside_dev * (trading_days_per_year**0.5)

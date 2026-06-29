"""Risk analytics — ATH-REL-009 §5.3, REQ-STAT-RISK-001."""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class RiskMetrics:
    """Portfolio/strategy risk summary — FR-001."""

    max_drawdown: float
    average_drawdown: float
    max_drawdown_duration: int
    volatility: float
    downside_volatility: float
    var_95: float
    cvar_95: float
    tail_ratio: float | None


def compute_risk_metrics(
    equity_curve: pd.DataFrame,
    *,
    trading_days_per_year: int = 252,
    var_confidence: float = 0.95,
) -> RiskMetrics:
    """Compute risk metrics from equity curve — REQ-STAT-RISK-001."""
    if equity_curve.empty or "equity" not in equity_curve.columns:
        return RiskMetrics(
            max_drawdown=0.0,
            average_drawdown=0.0,
            max_drawdown_duration=0,
            volatility=0.0,
            downside_volatility=0.0,
            var_95=0.0,
            cvar_95=0.0,
            tail_ratio=None,
        )

    equity = equity_curve["equity"].astype(float)
    daily_returns = equity.pct_change().dropna().to_numpy()

    rolling_max = equity.cummax()
    drawdown = (equity - rolling_max) / rolling_max
    max_dd = float(drawdown.min())
    negative_dd = drawdown[drawdown < 0]
    avg_dd = float(negative_dd.mean()) if len(negative_dd) else 0.0
    max_duration = _max_drawdown_duration(drawdown.to_numpy())

    vol = 0.0
    downside_vol = 0.0
    if len(daily_returns) > 1:
        vol = float(daily_returns.std(ddof=1) * math.sqrt(trading_days_per_year))
        downside = daily_returns[daily_returns < 0]
        if len(downside) > 0:
            downside_vol = float(downside.std(ddof=1) * math.sqrt(trading_days_per_year))

    var_95 = 0.0
    cvar_95 = 0.0
    tail_ratio: float | None = None
    if len(daily_returns) > 0:
        alpha = 1.0 - var_confidence
        var_95 = float(np.quantile(daily_returns, alpha))
        tail = daily_returns[daily_returns <= var_95]
        cvar_95 = float(tail.mean()) if len(tail) else var_95
        p95 = float(np.quantile(daily_returns, 0.95))
        p05 = float(np.quantile(daily_returns, 0.05))
        if p05 < 0:
            tail_ratio = abs(p95 / p05)

    return RiskMetrics(
        max_drawdown=max_dd,
        average_drawdown=avg_dd,
        max_drawdown_duration=max_duration,
        volatility=vol,
        downside_volatility=downside_vol,
        var_95=var_95,
        cvar_95=cvar_95,
        tail_ratio=tail_ratio,
    )


def _max_drawdown_duration(drawdown: np.ndarray) -> int:
    max_len = 0
    current = 0
    for d in drawdown:
        if d < 0:
            current += 1
            max_len = max(max_len, current)
        else:
            current = 0
    return max_len

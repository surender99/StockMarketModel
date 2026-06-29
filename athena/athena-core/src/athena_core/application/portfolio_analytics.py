"""Portfolio performance analytics — ATH-REL-008 §5.11."""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class PortfolioAnalytics:
    """Portfolio-level analytics snapshot — FR-007."""

    total_return: float
    volatility: float
    sharpe: float | None
    sortino: float | None
    max_drawdown: float
    calmar: float | None
    beta: float | None
    alpha: float | None
    information_ratio: float | None
    tracking_error: float | None
    diversification_ratio: float | None


def compute_portfolio_analytics(
    returns: pd.DataFrame,
    weights: dict[str, float],
    *,
    benchmark_returns: pd.Series | None = None,
    trading_days_per_year: int = 252,
) -> PortfolioAnalytics:
    """Compute portfolio analytics from asset returns — ATH-REL-008 §5.11."""
    symbols = [s for s in weights if s in returns.columns]
    if not symbols:
        return PortfolioAnalytics(
            total_return=0.0,
            volatility=0.0,
            sharpe=None,
            sortino=None,
            max_drawdown=0.0,
            calmar=None,
            beta=None,
            alpha=None,
            information_ratio=None,
            tracking_error=None,
            diversification_ratio=None,
        )

    w = np.array([weights[s] for s in symbols], dtype=float)
    asset_rets = returns[symbols].astype(float)
    port_rets = asset_rets.to_numpy(dtype=float) @ w
    port_series = pd.Series(port_rets, index=returns.index)

    total_return = float((1.0 + port_series).prod() - 1.0)
    volatility = float(port_series.std() * math.sqrt(trading_days_per_year))

    sharpe: float | None = None
    sortino: float | None = None
    if len(port_series) > 1 and port_series.std() > 0:
        sharpe = float(
            (port_series.mean() / port_series.std()) * math.sqrt(trading_days_per_year)
        )
        downside = port_series[port_series < 0]
        if len(downside) > 0 and downside.std() > 0:
            sortino = float(
                (port_series.mean() / downside.std()) * math.sqrt(trading_days_per_year)
            )

    equity = (1.0 + port_series).cumprod()
    rolling_max = equity.cummax()
    drawdown = (equity - rolling_max) / rolling_max
    max_drawdown = float(drawdown.min())

    years = max(len(port_series) / trading_days_per_year, 1.0 / trading_days_per_year)
    cagr = float((1.0 + total_return) ** (1.0 / years) - 1.0) if years > 0 else 0.0
    calmar: float | None = None
    if max_drawdown < 0:
        calmar = float(cagr / abs(max_drawdown))

    beta: float | None = None
    alpha: float | None = None
    information_ratio: float | None = None
    tracking_error: float | None = None
    if benchmark_returns is not None and len(benchmark_returns) == len(port_series):
        bench = benchmark_returns.astype(float)
        if bench.std() > 0:
            cov = float(port_series.cov(bench))
            bench_var = float(bench.var())
            beta = cov / bench_var if bench_var > 0 else None
            if beta is not None:
                alpha = float(port_series.mean() - beta * bench.mean()) * trading_days_per_year
        active = port_series - bench
        if active.std() > 0:
            tracking_error = float(active.std() * math.sqrt(trading_days_per_year))
            information_ratio = float(
                (active.mean() / active.std()) * math.sqrt(trading_days_per_year)
            )

    div_ratio: float | None = None
    asset_vols = asset_rets.std()
    weighted_vol_sum = float(sum(weights[s] * asset_vols[s] for s in symbols))
    if weighted_vol_sum > 0 and port_series.std() > 0:
        div_ratio = weighted_vol_sum / float(port_series.std())

    return PortfolioAnalytics(
        total_return=total_return,
        volatility=volatility,
        sharpe=sharpe,
        sortino=sortino,
        max_drawdown=max_drawdown,
        calmar=calmar,
        beta=beta,
        alpha=alpha,
        information_ratio=information_ratio,
        tracking_error=tracking_error,
        diversification_ratio=div_ratio,
    )

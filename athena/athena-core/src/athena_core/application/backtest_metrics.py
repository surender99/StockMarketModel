"""Backtest performance metrics — REQ-BT-ENGINE-001."""

from __future__ import annotations

import math
from datetime import date

import pandas as pd

from athena_core.domain.backtest import TradeRecord


def compute_metrics(
    equity_curve: pd.DataFrame,
    trades: list[TradeRecord],
    *,
    initial_capital: float,
    trading_days_per_year: int = 252,
) -> dict[str, float | int | None]:
    """Compute summary metrics from equity curve and trade log."""
    if equity_curve.empty:
        return {
            "total_return": 0.0,
            "cagr": 0.0,
            "max_drawdown": 0.0,
            "sharpe": None,
            "win_rate": None,
            "profit_factor": None,
            "trade_count": 0,
        }

    equity = equity_curve["equity"].astype(float)
    total_return = float(equity.iloc[-1] / initial_capital - 1.0)

    start_date = equity_curve["date"].iloc[0]
    end_date = equity_curve["date"].iloc[-1]
    years = _years_between(start_date, end_date)
    cagr = float((equity.iloc[-1] / initial_capital) ** (1.0 / years) - 1.0) if years > 0 else 0.0

    rolling_max = equity.cummax()
    drawdown = (equity - rolling_max) / rolling_max
    max_drawdown = float(drawdown.min())

    daily_returns = equity.pct_change().dropna()
    sharpe: float | None = None
    if len(daily_returns) > 1 and daily_returns.std() > 0:
        sharpe = float(
            (daily_returns.mean() / daily_returns.std()) * math.sqrt(trading_days_per_year)
        )

    wins = [t for t in trades if t.net_pnl > 0]
    losses = [t for t in trades if t.net_pnl <= 0]
    win_rate: float | None = None
    profit_factor: float | None = None
    if trades:
        win_rate = len(wins) / len(trades)
        gross_profit = sum(t.net_pnl for t in wins)
        gross_loss = abs(sum(t.net_pnl for t in losses))
        profit_factor = gross_profit / gross_loss if gross_loss > 0 else None

    return {
        "total_return": total_return,
        "cagr": cagr,
        "max_drawdown": max_drawdown,
        "sharpe": sharpe,
        "win_rate": win_rate,
        "profit_factor": profit_factor,
        "trade_count": len(trades),
    }


def compute_benchmark_metrics(
    benchmark_prices: pd.DataFrame,
    *,
    initial_capital: float,
    trading_days_per_year: int = 252,
) -> dict[str, float | None]:
    """Buy-and-hold benchmark metrics over the same date range."""
    if benchmark_prices.empty:
        return {"benchmark_total_return": None, "benchmark_cagr": None}

    prices = benchmark_prices.sort_values("date")["close"].astype(float)
    total_return = float(prices.iloc[-1] / prices.iloc[0] - 1.0)
    start_date = benchmark_prices["date"].iloc[0]
    end_date = benchmark_prices["date"].iloc[-1]
    years = _years_between(start_date, end_date)
    cagr = float((prices.iloc[-1] / prices.iloc[0]) ** (1.0 / years) - 1.0) if years > 0 else 0.0
    daily_returns = prices.pct_change().dropna()
    sharpe: float | None = None
    if len(daily_returns) > 1 and daily_returns.std() > 0:
        sharpe = float(
            (daily_returns.mean() / daily_returns.std()) * math.sqrt(trading_days_per_year)
        )
    return {
        "benchmark_total_return": total_return,
        "benchmark_cagr": cagr,
        "benchmark_sharpe": sharpe,
    }


def _years_between(start: date, end: date) -> float:
    days = (end - start).days
    return max(days / 365.25, 1.0 / 365.25)

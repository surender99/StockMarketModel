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

    advanced = compute_advanced_metrics(
        equity_curve,
        trades,
        initial_capital=initial_capital,
        max_drawdown=max_drawdown,
        cagr=cagr,
        trading_days_per_year=trading_days_per_year,
    )

    return {
        "total_return": total_return,
        "cagr": cagr,
        "max_drawdown": max_drawdown,
        "sharpe": sharpe,
        "win_rate": win_rate,
        "profit_factor": profit_factor,
        "trade_count": len(trades),
        **advanced,
    }


def compute_advanced_metrics(
    equity_curve: pd.DataFrame,
    trades: list[TradeRecord],
    *,
    initial_capital: float,
    max_drawdown: float,
    cagr: float,
    trading_days_per_year: int = 252,
) -> dict[str, float | None]:
    """Extended performance metrics — ATH-REL-007 §5.11, FR-011."""
    if equity_curve.empty:
        return {
            "sortino": None,
            "calmar": None,
            "recovery_factor": None,
            "ulcer_index": None,
            "average_trade": None,
            "expectancy": None,
        }

    equity = equity_curve["equity"].astype(float)
    daily_returns = equity.pct_change().dropna()

    sortino: float | None = None
    if len(daily_returns) > 1:
        downside = daily_returns[daily_returns < 0]
        if len(downside) > 0 and downside.std() > 0:
            sortino = float(
                (daily_returns.mean() / downside.std()) * math.sqrt(trading_days_per_year)
            )

    calmar: float | None = None
    if max_drawdown < 0:
        calmar = float(cagr / abs(max_drawdown))

    total_return = float(equity.iloc[-1] / initial_capital - 1.0)
    recovery_factor: float | None = None
    if max_drawdown < 0:
        recovery_factor = float(total_return / abs(max_drawdown))

    rolling_max = equity.cummax()
    drawdown_pct = ((equity - rolling_max) / rolling_max * 100.0).astype(float)
    ulcer_index = float((drawdown_pct**2).mean() ** 0.5) if len(drawdown_pct) else None

    average_trade: float | None = None
    expectancy: float | None = None
    if trades:
        average_trade = float(sum(t.net_pnl for t in trades) / len(trades))
        wins = [t.net_pnl for t in trades if t.net_pnl > 0]
        losses = [t.net_pnl for t in trades if t.net_pnl <= 0]
        win_rate = len(wins) / len(trades)
        avg_win = sum(wins) / len(wins) if wins else 0.0
        avg_loss = sum(losses) / len(losses) if losses else 0.0
        expectancy = float(win_rate * avg_win + (1.0 - win_rate) * avg_loss)

    return {
        "sortino": sortino,
        "calmar": calmar,
        "recovery_factor": recovery_factor,
        "ulcer_index": ulcer_index,
        "average_trade": average_trade,
        "expectancy": expectancy,
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

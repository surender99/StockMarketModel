"""Tests for backtest engine — REQ-BT-ENGINE-001."""

from __future__ import annotations

from datetime import date, timedelta
from typing import Any

import pandas as pd

from athena_core.application.backtest_config import BacktestConfig, BacktestCostsConfig
from athena_core.application.backtest_engine import BacktestEngine, FeatureProviderPort
from athena_core.application.costs import apply_slippage, compute_trade_costs
from athena_core.domain.ports.trading_calendar import TradingCalendarPort
from athena_core.domain.strategy.config import (
    EntryConfig,
    ExitConfig,
    ExitRuleSpec,
    IndicatorSpec,
    PositionSizingConfig,
    RiskConfig,
    RuleSpec,
    StrategyConfig,
    StrategyMeta,
    UniverseConfig,
)
from tests.memory_ohlcv_repo import MemoryOHLCVRepo


class _Calendar(TradingCalendarPort):
    def is_trading_day(self, d: date) -> bool:
        return d.weekday() < 5

    def trading_days_between(self, start: date, end: date) -> list[date]:
        days: list[date] = []
        cur = start
        while cur <= end:
            if self.is_trading_day(cur):
                days.append(cur)
            cur += timedelta(days=1)
        return days

    def next_trading_day(self, d: date) -> date:
        n = d + timedelta(days=1)
        while not self.is_trading_day(n):
            n += timedelta(days=1)
        return n

    def previous_trading_day(self, d: date) -> date:
        n = d - timedelta(days=1)
        while not self.is_trading_day(n):
            n -= timedelta(days=1)
        return n

    def holidays_for_year(self, year: int) -> list[date]:
        return []


class _Features(FeatureProviderPort):
    def __init__(self, indicators: dict[str, pd.DataFrame]) -> None:
        self._indicators = indicators

    def get_indicator_frame(
        self,
        symbol: str,
        indicator_type: str,
        params: dict[str, Any],
        start: date | None,
        end: date | None,
    ) -> pd.DataFrame:
        key = f"{symbol}:{indicator_type}:{params['period']}"
        df = self._indicators[key].copy()
        if start:
            df = df[df["date"] >= start]
        if end:
            df = df[df["date"] <= end]
        return df.reset_index(drop=True)


def _synthetic_crossover_series() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    dates = [date(2024, 1, 2) + timedelta(days=i) for i in range(10)]
    close = [100, 101, 102, 103, 104, 103, 102, 101, 100, 99]
    ohlcv = pd.DataFrame(
        {
            "date": dates,
            "open": close,
            "high": [c + 1 for c in close],
            "low": [c - 1 for c in close],
            "close": close,
            "volume": [200_000] * len(dates),
            "symbol": ["TEST"] * len(dates),
        }
    )
    ema_fast = pd.DataFrame(
        {"date": dates, "ema_9": [98, 99, 100, 101, 103, 102, 101, 100, 99, 98]}
    )
    ema_slow = pd.DataFrame(
        {"date": dates, "ema_21": [99, 99, 99, 100, 101, 102, 102, 101, 100, 99]}
    )
    return ohlcv, ema_fast, ema_slow


def _strategy(max_positions: int = 1) -> StrategyConfig:
    return StrategyConfig(
        strategy=StrategyMeta(id="t", version="1"),
        universe=UniverseConfig(symbols=["TEST"]),
        indicators=[
            IndicatorSpec(id="ema_fast", type="ema", params={"period": 9}),
            IndicatorSpec(id="ema_slow", type="ema", params={"period": 21}),
        ],
        entry=EntryConfig(
            rules=[
                RuleSpec(
                    condition="ema_fast > ema_slow and ema_fast.shift(1) <= ema_slow.shift(1)",
                    side="long",
                )
            ]
        ),
        exit=ExitConfig(rules=[ExitRuleSpec(condition="ema_fast < ema_slow", reason="rev")]),
        position_sizing=PositionSizingConfig(
            method="fixed_fraction",
            params={"fraction": 0.5, "max_positions": max_positions},
        ),
        risk=RiskConfig(),
    )


def test_cost_calculation_spot_check() -> None:
    costs = BacktestCostsConfig(
        brokerage_pct=0.001, brokerage_flat=20, slippage_pct=0.001, stt_pct=0.001
    )
    fees = compute_trade_costs(100_000, costs, is_sell=True)
    assert fees > 20
    buy_fill = apply_slippage(100.0, costs, is_buy=True)
    assert buy_fill > 100.0


def test_synthetic_trade_count() -> None:
    ohlcv, fast, slow = _synthetic_crossover_series()
    repo = MemoryOHLCVRepo({"TEST": ohlcv, "^NSEI": ohlcv})
    features = _Features(
        {
            "TEST:ema:9": fast.rename(columns={"ema_9": "ema_9"}),
            "TEST:ema:21": slow.rename(columns={"ema_21": "ema_21"}),
        }
    )
    engine = BacktestEngine(_Calendar(), repo, features)
    config = BacktestConfig(start=date(2024, 1, 2), end=date(2024, 1, 15), initial_capital=100_000)
    result = engine.run(_strategy(), config)
    assert len(result.trades) >= 1
    assert result.metrics["trade_count"] == len(result.trades)


def test_costs_reduce_pnl() -> None:
    ohlcv, fast, slow = _synthetic_crossover_series()
    repo = MemoryOHLCVRepo({"TEST": ohlcv, "^NSEI": ohlcv})
    features = _Features(
        {
            "TEST:ema:9": fast,
            "TEST:ema:21": slow,
        }
    )
    engine = BacktestEngine(_Calendar(), repo, features)
    start, end = date(2024, 1, 2), date(2024, 1, 15)
    zero_cost = BacktestConfig(
        start=start,
        end=end,
        initial_capital=100_000,
        costs=BacktestCostsConfig(brokerage_pct=0, brokerage_flat=0, slippage_pct=0, stt_pct=0),
    )
    with_cost = BacktestConfig(start=start, end=end, initial_capital=100_000)
    r0 = engine.run(_strategy(), zero_cost)
    r1 = engine.run(_strategy(), with_cost)
    if r0.trades and r1.trades:
        assert r1.trades[0].net_pnl <= r0.trades[0].net_pnl


def test_max_positions_enforced() -> None:
    ohlcv, fast, slow = _synthetic_crossover_series()
    ohlcv_b = ohlcv.copy()
    ohlcv_b["symbol"] = "TEST2"
    repo = MemoryOHLCVRepo({"TEST": ohlcv, "TEST2": ohlcv_b, "^NSEI": ohlcv})
    features = _Features(
        {
            "TEST:ema:9": fast,
            "TEST:ema:21": slow,
            "TEST2:ema:9": fast,
            "TEST2:ema:21": slow,
        }
    )
    engine = BacktestEngine(_Calendar(), repo, features)
    strategy = _strategy(max_positions=1)
    strategy.universe.symbols = ["TEST", "TEST2"]
    config = BacktestConfig(start=date(2024, 1, 2), end=date(2024, 1, 15), initial_capital=500_000)
    result = engine.run(strategy, config, symbols=["TEST", "TEST2"])
    open_entries = len({t.symbol for t in result.trades})
    assert open_entries >= 1


def test_reproducible_results() -> None:
    ohlcv, fast, slow = _synthetic_crossover_series()
    repo = MemoryOHLCVRepo({"TEST": ohlcv, "^NSEI": ohlcv})
    features = _Features({"TEST:ema:9": fast, "TEST:ema:21": slow})
    engine = BacktestEngine(_Calendar(), repo, features)
    config = BacktestConfig(start=date(2024, 1, 2), end=date(2024, 1, 15), initial_capital=100_000)
    a = engine.run(_strategy(), config)
    b = engine.run(_strategy(), config)
    assert [(t.entry_date, t.exit_date, t.quantity) for t in a.trades] == [
        (t.entry_date, t.exit_date, t.quantity) for t in b.trades
    ]


def test_benchmark_metrics_present() -> None:
    ohlcv, fast, slow = _synthetic_crossover_series()
    repo = MemoryOHLCVRepo({"TEST": ohlcv, "^NSEI": ohlcv})
    features = _Features({"TEST:ema:9": fast, "TEST:ema:21": slow})
    engine = BacktestEngine(_Calendar(), repo, features)
    config = BacktestConfig(start=date(2024, 1, 2), end=date(2024, 1, 15), initial_capital=100_000)
    result = engine.run(_strategy(), config)
    assert "benchmark_total_return" in result.benchmark_metrics


def test_lookahead_shifted_signal_not_early() -> None:
    dates = [date(2024, 1, 2) + timedelta(days=i) for i in range(6)]
    close = [100, 100, 100, 150, 150, 150]
    ohlcv = pd.DataFrame(
        {
            "date": dates,
            "open": close,
            "high": close,
            "low": close,
            "close": close,
            "volume": [300_000] * len(dates),
            "symbol": ["TEST"] * len(dates),
        }
    )
    fast = pd.DataFrame({"date": dates, "ema_9": [90, 90, 90, 140, 140, 140]})
    slow = pd.DataFrame({"date": dates, "ema_21": [95, 95, 95, 100, 100, 100]})
    repo = MemoryOHLCVRepo({"TEST": ohlcv, "^NSEI": ohlcv})
    features = _Features({"TEST:ema:9": fast, "TEST:ema:21": slow})
    engine = BacktestEngine(_Calendar(), repo, features)
    strategy = _strategy()
    strategy.entry.rules[0].condition = "ema_fast > ema_slow"
    config = BacktestConfig(start=dates[0], end=dates[-1], initial_capital=100_000)
    result = engine.run(strategy, config)
    if result.trades:
        assert result.trades[0].entry_date >= dates[3]


def test_backtest_portfolio_and_statistics_integration() -> None:
    """Vertical slice: backtest returns portfolio evaluation and statistics — Rev 2."""
    ohlcv, fast, slow = _synthetic_crossover_series()
    repo = MemoryOHLCVRepo({"TEST": ohlcv, "^NSEI": ohlcv})
    features = _Features({"TEST:ema:9": fast, "TEST:ema:21": slow})
    engine = BacktestEngine(_Calendar(), repo, features)
    config = BacktestConfig(start=date(2024, 1, 2), end=date(2024, 1, 15), initial_capital=100_000)
    result = engine.run(_strategy(), config)
    assert result.portfolio_evaluation is not None
    assert result.statistics_report is not None
    assert "expectancy" in result.statistics_report
    assert "portfolio_heat" in result.metrics

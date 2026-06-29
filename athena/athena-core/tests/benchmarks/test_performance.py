"""Performance benchmark tests — Rev 2 targets."""

from __future__ import annotations

import time
from datetime import date, timedelta

import pandas as pd
import pytest

from athena_core.application.backtest_config import BacktestConfig, BacktestCostsConfig
from athena_core.application.backtest_engine import BacktestEngine, FeatureProviderPort
from athena_core.application.config import FeatureStoreConfig
from athena_core.application.feature_service import FeatureService
from athena_core.domain.features.indicator_plugins import register_builtin_indicators
from athena_core.domain.plugins import PluginRegistry
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
from athena_core.infrastructure.parquet_feature_store import ParquetFeatureStore
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
    def __init__(self, service: FeatureService) -> None:
        self._service = service

    def get_indicator_frame(
        self,
        symbol: str,
        indicator_type: str,
        params: dict,
        start: date | None,
        end: date | None,
    ) -> pd.DataFrame:
        return self._service.get_feature(symbol, indicator_type, params, start=start, end=end)


def _synthetic_ohlcv(days: int = 252) -> pd.DataFrame:
    dates = pd.bdate_range("2023-01-02", periods=days).date
    close = [100.0 + i * 0.1 for i in range(days)]
    return pd.DataFrame(
        {
            "date": dates,
            "open": close,
            "high": [c + 1 for c in close],
            "low": [c - 1 for c in close],
            "close": close,
            "volume": [1_000_000] * days,
            "symbol": ["SYM"] * days,
        }
    )


@pytest.mark.benchmark
def test_indicator_generation_under_2s(tmp_path) -> None:
    repo = MemoryOHLCVRepo({"SYM": _synthetic_ohlcv()})
    store = ParquetFeatureStore(tmp_path, "snappy")
    registry = PluginRegistry()
    register_builtin_indicators(registry)
    service = FeatureService(store, repo, FeatureStoreConfig(), plugin_registry=registry)
    start = time.perf_counter()
    frame = service.get_feature(
        "SYM", "ema", {"period": 20}, start=date(2023, 1, 2), end=date(2023, 12, 31)
    )
    elapsed = time.perf_counter() - start
    assert not frame.empty
    assert elapsed < 2.0, f"indicator generation took {elapsed:.2f}s"


@pytest.mark.benchmark
def test_backtest_small_universe_reasonable_time(tmp_path) -> None:
    symbols = [f"S{i}" for i in range(5)]
    frames = {s: _synthetic_ohlcv(120) for s in symbols}
    for df in frames.values():
        df["symbol"] = df["symbol"].iloc[0]
    repo = MemoryOHLCVRepo(frames)
    store = ParquetFeatureStore(tmp_path, "snappy")
    registry = PluginRegistry()
    register_builtin_indicators(registry)
    service = FeatureService(store, repo, FeatureStoreConfig(), plugin_registry=registry)
    strategy = StrategyConfig(
        strategy=StrategyMeta(id="bench", version="1"),
        universe=UniverseConfig(symbols=symbols),
        indicators=[IndicatorSpec(id="ema_fast", type="ema", params={"period": 10})],
        entry=EntryConfig(rules=[RuleSpec(condition="close > ema_fast", side="long")]),
        exit=ExitConfig(rules=[ExitRuleSpec(condition="close < ema_fast", reason="signal")]),
        position_sizing=PositionSizingConfig(
            method="fixed_fraction",
            params={"fraction": 0.1, "max_positions": 3},
        ),
        risk=RiskConfig(),
    )
    config = BacktestConfig(
        start=date(2023, 3, 1),
        end=date(2023, 8, 1),
        initial_capital=1_000_000.0,
        costs=BacktestCostsConfig(),
    )
    engine = BacktestEngine(_Calendar(), repo, _Features(service))
    start = time.perf_counter()
    result = engine.run(strategy, config, symbols=symbols)
    elapsed = time.perf_counter() - start
    assert result.statistics_report is not None
    assert elapsed < 15.0, f"backtest took {elapsed:.2f}s"

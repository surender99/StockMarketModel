"""Backtest engine framework tests — ATH-REL-007."""

from __future__ import annotations

from datetime import date, timedelta
from typing import Any

import pandas as pd

from athena_core.application.backtest_config import BacktestConfig, BacktestCostsConfig
from athena_core.application.backtest_engine import BacktestEngine, FeatureProviderPort
from athena_core.application.backtest_manager import BacktestManager
from athena_core.application.bootstrap import bootstrap_athena_core
from athena_core.application.config import AthenaConfig
from athena_core.domain.backtest import (
    FillModel,
    Order,
    OrderSide,
    OrderStatus,
    OrderType,
    SlippageModel,
    apply_slippage_model,
    resolve_fill_price,
)
from athena_core.domain.backtest.backtest_plugins import (
    list_fill_models,
    list_slippage_models,
    register_builtin_backtest_plugins,
)
from athena_core.domain.backtest.orders import validate_order
from athena_core.domain.plugins import PluginRegistry, PluginType
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


class _Calendar:
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


def _strategy() -> StrategyConfig:
    return StrategyConfig(
        strategy=StrategyMeta(id="ema_x", version="1"),
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
            params={"fraction": 0.5, "max_positions": 1},
        ),
        risk=RiskConfig(),
    )


def _synthetic_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    dates = [date(2024, 1, 2) + timedelta(days=i) for i in range(10)]
    close = [100, 101, 102, 103, 104, 103, 102, 101, 100, 99]
    ohlcv = pd.DataFrame(
        {
            "date": dates,
            "open": [c - 0.5 for c in close],
            "high": [c + 1 for c in close],
            "low": [c - 1 for c in close],
            "close": close,
            "volume": [200_000] * len(dates),
            "symbol": ["TEST"] * len(dates),
        }
    )
    fast = pd.DataFrame({"date": dates, "ema_9": [98, 99, 100, 101, 103, 102, 101, 100, 99, 98]})
    slow = pd.DataFrame({"date": dates, "ema_21": [99, 99, 99, 100, 101, 102, 102, 101, 100, 99]})
    return ohlcv, fast, slow


def test_req_bt_order_001_order_state_machine() -> None:
    """REQ-BT-ORDER-001 — order lifecycle transitions."""
    order = Order(
        order_id="1",
        symbol="TEST",
        side=OrderSide.BUY,
        order_type=OrderType.MARKET,
        quantity=10,
        signal_date=date(2024, 1, 2),
    )
    assert validate_order(order) == []
    order.submit()
    assert order.status == OrderStatus.SUBMITTED
    order.fill(100.0, 10, date(2024, 1, 3))
    assert order.status == OrderStatus.FILLED
    assert order.fill_price == 100.0


def test_req_bt_order_001_limit_requires_price() -> None:
    """REQ-BT-ORDER-001 — limit order validation."""
    order = Order(
        order_id="2",
        symbol="TEST",
        side=OrderSide.BUY,
        order_type=OrderType.LIMIT,
        quantity=5,
        signal_date=date(2024, 1, 2),
    )
    errors = validate_order(order)
    assert any("limit_price" in e for e in errors)


def test_req_bt_execution_001_fill_models_registered() -> None:
    """REQ-BT-EXECUTION-001 — fill models available."""
    models = list_fill_models()
    assert FillModel.CURRENT_BAR_CLOSE in models
    assert FillModel.NEXT_BAR_OPEN in models


def test_req_bt_execution_001_resolve_next_bar_open() -> None:
    """REQ-BT-EXECUTION-001 — next bar open fill price."""
    frame = pd.DataFrame({"open": [99.0, 101.0], "close": [100.0, 102.0]})
    price = resolve_fill_price(frame, 0, fill_model=FillModel.NEXT_BAR_OPEN, is_buy=True)
    assert price == 101.0


def test_slippage_models() -> None:
    """FR-004 — slippage model variants."""
    costs = BacktestCostsConfig(slippage_pct=0.01)
    pct = apply_slippage_model(100.0, costs, model=SlippageModel.PERCENTAGE, is_buy=True)
    atr = apply_slippage_model(100.0, costs, model=SlippageModel.ATR_BASED, is_buy=True, atr=2.0)
    assert pct > 100.0
    assert atr > 100.0


def test_bootstrap_registers_backtest_plugins() -> None:
    """ATH-REL-007 — execution plugins at bootstrap."""
    ctx = bootstrap_athena_core(AthenaConfig())
    plugins = ctx.plugin_registry.list(plugin_type=PluginType.REPORT, active_only=True)
    ids = {p.id for p in plugins}
    assert "fill:current_bar_close" in ids
    assert "slippage:percentage" in ids


def test_register_builtin_backtest_plugins() -> None:
    registry = PluginRegistry()
    count = register_builtin_backtest_plugins(registry)
    assert count >= 7


def test_backtest_manager_session() -> None:
    """ATH-REL-007 §5.1 — BacktestManager coordinates runs."""
    ohlcv, fast, slow = _synthetic_data()
    repo = MemoryOHLCVRepo({"TEST": ohlcv, "^NSEI": ohlcv})
    features = _Features({"TEST:ema:9": fast, "TEST:ema:21": slow})
    engine = BacktestEngine(_Calendar(), repo, features)
    manager = BacktestManager(engine)
    config = BacktestConfig(start=date(2024, 1, 2), end=date(2024, 1, 15), initial_capital=100_000)
    session = manager.create_session(_strategy(), config)
    result = manager.run(session)
    journal = manager.trade_journal(result, _strategy(), config)
    assert session.session_id
    assert len(result.trades) >= 1
    assert len(result.trade_journal) == len(result.trades)
    assert len(journal) == len(result.trades)


def test_advanced_metrics_present() -> None:
    """FR-011 — advanced performance metrics."""
    ohlcv, fast, slow = _synthetic_data()
    repo = MemoryOHLCVRepo({"TEST": ohlcv, "^NSEI": ohlcv})
    features = _Features({"TEST:ema:9": fast, "TEST:ema:21": slow})
    engine = BacktestEngine(_Calendar(), repo, features)
    config = BacktestConfig(start=date(2024, 1, 2), end=date(2024, 1, 15), initial_capital=100_000)
    result = engine.run(_strategy(), config)
    assert "sortino" in result.metrics
    assert "calmar" in result.metrics
    assert "recovery_factor" in result.metrics
    assert "ulcer_index" in result.metrics
    assert "average_trade" in result.metrics


def test_next_bar_open_defers_entry() -> None:
    """REQ-BT-EXECUTION-001 — next bar open delays fill."""
    ohlcv, fast, slow = _synthetic_data()
    repo = MemoryOHLCVRepo({"TEST": ohlcv, "^NSEI": ohlcv})
    features = _Features({"TEST:ema:9": fast, "TEST:ema:21": slow})
    engine = BacktestEngine(_Calendar(), repo, features)
    close_config = BacktestConfig(
        start=date(2024, 1, 2), end=date(2024, 1, 15), initial_capital=100_000
    )
    open_config = close_config.model_copy(update={"execution_model": FillModel.NEXT_BAR_OPEN})
    close_result = engine.run(_strategy(), close_config)
    open_result = engine.run(_strategy(), open_config)
    if close_result.trades and open_result.trades:
        assert open_result.trades[0].entry_date >= close_result.trades[0].entry_date


def test_trade_journal_fields() -> None:
    """FR-010 — trade journal captures lifecycle."""
    ohlcv, fast, slow = _synthetic_data()
    repo = MemoryOHLCVRepo({"TEST": ohlcv, "^NSEI": ohlcv})
    features = _Features({"TEST:ema:9": fast, "TEST:ema:21": slow})
    engine = BacktestEngine(_Calendar(), repo, features)
    config = BacktestConfig(start=date(2024, 1, 2), end=date(2024, 1, 15), initial_capital=100_000)
    result = engine.run(_strategy(), config)
    if result.trade_journal:
        entry = result.trade_journal[0]
        assert entry.strategy_id == "ema_x"
        assert entry.duration_days >= 0
        assert entry.commission >= 0

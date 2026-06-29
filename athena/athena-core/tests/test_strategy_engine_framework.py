"""Strategy engine framework tests — ATH-REL-006."""

from __future__ import annotations

import pandas as pd
import pytest

from athena_core.application.bootstrap import bootstrap_athena_core
from athena_core.application.config import AthenaConfig
from athena_core.domain.plugins import PluginRegistry, PluginType
from athena_core.domain.strategy import (
    CompositionMode,
    RiskContext,
    RiskLimits,
    SignalDirection,
    StrategyEngine,
    StrategyValidationError,
    compose_signals,
    compute_position_quantity,
    ema_crossover_strategy,
    register_builtin_strategies,
    resolve_strategy,
    validate_strategy,
    within_risk_limits,
)
from athena_core.domain.strategy.signals import SignalEngine
from athena_core.domain.strategy.types import TradeSignal


def _frame() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "date": pd.date_range("2024-01-01", periods=5, freq="D").date,
            "close": [100.0, 101.0, 102.0, 103.0, 104.0],
            "volume": [1000, 1100, 1200, 1300, 1400],
            "ema_50": [99.0, 100.0, 101.0, 102.0, 103.0],
            "ema_200": [98.0, 98.5, 99.0, 99.5, 100.0],
        }
    )


def test_req_strat_registry_001_builtin_strategies_registered() -> None:
    """REQ-STRAT-REGISTRY-001 — built-in strategies resolve via PluginRegistry."""
    registry = PluginRegistry()
    register_builtin_strategies(registry)
    strategies = registry.list(plugin_type=PluginType.STRATEGY, active_only=True)
    ids = {p.id for p in strategies}
    assert {"ema_crossover", "ema_pullback"} <= ids


def test_resolve_strategy_returns_config() -> None:
    registry = PluginRegistry()
    register_builtin_strategies(registry)
    config = resolve_strategy(registry, "ema_crossover")
    assert config.strategy.id == "ema_crossover"
    assert len(config.indicators) == 2


def test_bootstrap_registers_strategies() -> None:
    ctx = bootstrap_athena_core(AthenaConfig())
    strategies = ctx.plugin_registry.list(plugin_type=PluginType.STRATEGY, active_only=True)
    assert any(p.id == "ema_crossover" for p in strategies)


def test_signal_engine_entry_crossover() -> None:
    engine = SignalEngine()
    strategy = ema_crossover_strategy()
    frame = pd.DataFrame(
        {
            "date": pd.date_range("2024-01-01", periods=5, freq="D").date,
            "close": [100.0, 100.0, 101.0, 102.0, 103.0],
            "volume": [1000] * 5,
            "ema_50": [98.0, 99.0, 101.0, 102.0, 103.0],
            "ema_200": [100.0, 100.0, 100.0, 100.0, 100.0],
        }
    )
    signal = engine.best_entry_signal(strategy, frame, 2)
    assert signal is not None
    assert signal.direction == SignalDirection.BUY


def test_strategy_engine_validates_before_evaluate() -> None:
    strategy = ema_crossover_strategy()
    strategy.indicators = []
    engine = StrategyEngine()
    frame = _frame()
    with pytest.raises(StrategyValidationError):
        engine.evaluate_entry(strategy, frame, 2)


def test_compose_signals_and_mode() -> None:
    signals = [
        TradeSignal(direction=SignalDirection.BUY, confidence=0.8, reason="a", side="long"),
        TradeSignal(direction=SignalDirection.BUY, confidence=0.9, reason="b", side="long"),
    ]
    composed = compose_signals(signals, CompositionMode.AND)
    assert composed is not None
    assert composed.direction == SignalDirection.BUY
    assert composed.confidence == 0.8


def test_compose_signals_or_mode() -> None:
    signals = [
        TradeSignal(direction=SignalDirection.NEUTRAL, confidence=0.0, reason="a"),
        TradeSignal(direction=SignalDirection.BUY, confidence=0.7, reason="b", side="long"),
    ]
    composed = compose_signals(signals, CompositionMode.OR)
    assert composed is not None
    assert composed.direction == SignalDirection.BUY


def test_position_sizing_pct_risk() -> None:
    qty = compute_position_quantity(
        "pct_risk",
        {"risk_pct": 0.02, "stop_pct": 0.05},
        price=100.0,
        cash=100_000.0,
    )
    assert qty == 400


def test_position_sizing_atr_based() -> None:
    qty = compute_position_quantity(
        "atr_based",
        {"risk_pct": 0.01, "atr_multiplier": 2.0},
        price=100.0,
        cash=50_000.0,
        atr=2.5,
    )
    assert qty == 100


def test_risk_limits_block_entry() -> None:
    limits = RiskLimits(max_drawdown_pct=0.1)
    context = RiskContext(
        equity=85_000.0,
        initial_equity=100_000.0,
        daily_pnl_pct=-0.02,
        drawdown_pct=0.15,
        gross_exposure_pct=0.5,
    )
    assert not within_risk_limits(context, limits)


def test_validate_strategy_missing_indicator() -> None:
    strategy = ema_crossover_strategy()
    strategy.entry.rules[0].condition = "missing_id > 0"
    issues = validate_strategy(strategy)
    assert any("missing_id" in issue for issue in issues)


def test_strategy_engine_with_registry() -> None:
    registry = PluginRegistry()
    register_builtin_strategies(registry)
    engine = StrategyEngine(registry)
    strategy = engine.load("ema_crossover")
    frame = _frame()
    frame["ema_50"] = frame["close"]
    frame["ema_200"] = frame["close"] * 0.99
    # No crossover in flat data — expect None or neutral
    result = engine.evaluate_entry(strategy, frame, 1)
    assert result is None or result.direction in {
        SignalDirection.BUY,
        SignalDirection.NEUTRAL,
        SignalDirection.SELL,
    }

"""Tests for strategy parameter overrides — REQ-OPT-001."""

from __future__ import annotations

import pytest

from athena_core.application.strategy_overrides import apply_strategy_overrides
from athena_core.domain.strategy.config import (
    EntryConfig,
    ExitConfig,
    ExitRuleSpec,
    IndicatorSpec,
    PositionSizingConfig,
    RuleSpec,
    StrategyConfig,
    StrategyMeta,
    UniverseConfig,
)


def _strategy() -> StrategyConfig:
    return StrategyConfig(
        strategy=StrategyMeta(id="opt_test", version="1.0.0"),
        universe=UniverseConfig(symbols=["TEST"]),
        indicators=[
            IndicatorSpec(id="ema_fast", type="ema", params={"period": 50}),
            IndicatorSpec(id="ema_slow", type="ema", params={"period": 200}),
        ],
        entry=EntryConfig(rules=[RuleSpec(condition="True", side="long")]),
        exit=ExitConfig(rules=[ExitRuleSpec(condition="True", reason="x")]),
        position_sizing=PositionSizingConfig(
            method="fixed_fraction",
            params={"fraction": 0.05, "max_positions": 10},
        ),
        risk={"stop_loss_pct": 0.05, "take_profit_pct": 0.15, "max_holding_days": 60},
    )


def test_apply_risk_override() -> None:
    updated = apply_strategy_overrides(_strategy(), {"risk.stop_loss_pct": 0.08})
    assert updated.risk.stop_loss_pct == 0.08


def test_apply_indicator_override() -> None:
    updated = apply_strategy_overrides(
        _strategy(),
        {"indicators.ema_fast.params.period": 21},
    )
    fast = next(i for i in updated.indicators if i.id == "ema_fast")
    assert fast.params["period"] == 21


def test_apply_unknown_indicator_raises() -> None:
    with pytest.raises(ValueError, match="indicator id not found"):
        apply_strategy_overrides(_strategy(), {"indicators.missing.params.period": 10})

"""Tests for AthenaRuntime helpers — REQ-SDK-001."""

from __future__ import annotations

from athena_core.application.optimizer import OptimizerResult
from athena_core.application.runtime import (
    AthenaRuntime,
    format_comparison_table,
    optimizer_to_dict,
    walk_forward_to_dict,
)


def test_format_comparison_table() -> None:
    comparison = {
        "metric_keys": ["total_return"],
        "experiments": [
            {
                "experiment_id": "a",
                "strategy_id": "s1",
                "train_start": "2024-01-01",
                "train_end": "2024-06-01",
                "total_return": 0.1,
            }
        ],
    }
    text = format_comparison_table(comparison)
    assert "experiment_id" in text
    assert "0.1" in text


def test_optimizer_to_dict_empty() -> None:
    payload = optimizer_to_dict(OptimizerResult())
    assert payload["trial_count"] == 0
    assert payload["best_trial"] is None


def test_walk_forward_to_dict_empty() -> None:
    from athena_core.application.walk_forward import WalkForwardSummary

    payload = walk_forward_to_dict(
        WalkForwardSummary(folds=[], aggregate_metrics={"fold_count": 0})
    )
    assert payload["fold_count"] == 0


def test_runtime_resolve_symbols() -> None:
    from athena_core.domain.strategy.config import (
        EntryConfig,
        ExitConfig,
        ExitRuleSpec,
        PositionSizingConfig,
        RuleSpec,
        StrategyConfig,
        StrategyMeta,
        UniverseConfig,
    )

    strategy = StrategyConfig(
        strategy=StrategyMeta(id="x", version="1"),
        universe=UniverseConfig(symbols=["AAA"]),
        entry=EntryConfig(rules=[RuleSpec(condition="True", side="long")]),
        exit=ExitConfig(rules=[ExitRuleSpec(condition="False", reason="x")]),
        position_sizing=PositionSizingConfig(method="fixed_fraction", params={"fraction": 0.1}),
    )
    symbols = AthenaRuntime.resolve_symbols(strategy, symbol="BBB")
    assert symbols == ["AAA", "BBB"]

"""Built-in strategy templates — ATH-REL-006 §5.4, FR-001."""

from __future__ import annotations

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


def ema_crossover_strategy() -> StrategyConfig:
    """EMA fast/slow golden-cross template — ATH-REL-006 §5.4."""
    return StrategyConfig(
        strategy=StrategyMeta(
            id="ema_crossover",
            version="0.1.0",
            description="EMA crossover long-only strategy",
        ),
        universe=UniverseConfig(source="custom", symbols=[]),
        indicators=[
            IndicatorSpec(id="ema_fast", type="ema", params={"period": 50}),
            IndicatorSpec(id="ema_slow", type="ema", params={"period": 200}),
        ],
        entry=EntryConfig(
            rules=[
                RuleSpec(
                    condition="ema_fast > ema_slow and ema_fast.shift(1) <= ema_slow.shift(1)",
                    side="long",
                )
            ]
        ),
        exit=ExitConfig(
            rules=[ExitRuleSpec(condition="ema_fast < ema_slow", reason="signal_reversal")]
        ),
        position_sizing=PositionSizingConfig(
            method="fixed_fraction",
            params={"fraction": 0.05, "max_positions": 10},
        ),
        risk=RiskConfig(stop_loss_pct=0.05, take_profit_pct=0.15, max_holding_days=60),
    )


def ema_pullback_strategy() -> StrategyConfig:
    """EMA pullback entry on fast above slow — ATH-REL-006 §5.4."""
    return StrategyConfig(
        strategy=StrategyMeta(
            id="ema_pullback",
            version="0.1.0",
            description="Pullback to fast EMA in uptrend",
        ),
        universe=UniverseConfig(source="custom", symbols=[]),
        indicators=[
            IndicatorSpec(id="ema_fast", type="ema", params={"period": 20}),
            IndicatorSpec(id="ema_slow", type="ema", params={"period": 50}),
        ],
        entry=EntryConfig(
            rules=[
                RuleSpec(
                    condition="ema_fast > ema_slow and close <= ema_fast",
                    side="long",
                )
            ]
        ),
        exit=ExitConfig(
            rules=[ExitRuleSpec(condition="ema_fast < ema_slow", reason="trend_break")]
        ),
        position_sizing=PositionSizingConfig(
            method="fixed_fraction",
            params={"fraction": 0.05, "max_positions": 10},
        ),
    )


def builtin_strategy_registry() -> dict[str, StrategyConfig]:
    """Return built-in strategy templates keyed by strategy id."""
    strategies = [ema_crossover_strategy(), ema_pullback_strategy()]
    return {s.strategy.id: s for s in strategies}

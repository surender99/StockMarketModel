"""Strategy domain models — REQ-STRAT-CONFIG-001, ATH-REL-006."""

from athena_core.domain.strategy.builtin import builtin_strategy_registry, ema_crossover_strategy
from athena_core.domain.strategy.composition import CompositionMode, compose_signals
from athena_core.domain.strategy.config import (
    EntryConfig,
    ExitConfig,
    ExitRuleSpec,
    FilterSpec,
    IndicatorSpec,
    PositionSizingConfig,
    RiskConfig,
    RuleSpec,
    StrategyConfig,
    StrategyMeta,
    UniverseConfig,
)
from athena_core.domain.strategy.engine import StrategyEngine
from athena_core.domain.strategy.expression import evaluate_condition_at_index
from athena_core.domain.strategy.indicators import INDICATOR_TYPES, validate_indicator_specs
from athena_core.domain.strategy.position_sizing import compute_position_quantity
from athena_core.domain.strategy.risk import RiskContext, RiskLimits, check_risk_limits, within_risk_limits
from athena_core.domain.strategy.signals import SignalEngine
from athena_core.domain.strategy.strategy_plugins import (
    register_builtin_strategies,
    resolve_strategy,
)
from athena_core.domain.strategy.types import SignalDirection, TradeSignal
from athena_core.domain.strategy.validation import StrategyValidationError, validate_strategy

__all__ = [
    "CompositionMode",
    "EntryConfig",
    "ExitConfig",
    "ExitRuleSpec",
    "FilterSpec",
    "INDICATOR_TYPES",
    "IndicatorSpec",
    "PositionSizingConfig",
    "RiskConfig",
    "RiskContext",
    "RiskLimits",
    "RuleSpec",
    "SignalDirection",
    "SignalEngine",
    "StrategyConfig",
    "StrategyEngine",
    "StrategyMeta",
    "StrategyValidationError",
    "TradeSignal",
    "UniverseConfig",
    "builtin_strategy_registry",
    "check_risk_limits",
    "compose_signals",
    "compute_position_quantity",
    "ema_crossover_strategy",
    "evaluate_condition_at_index",
    "register_builtin_strategies",
    "resolve_strategy",
    "validate_indicator_specs",
    "validate_strategy",
    "within_risk_limits",
]

"""Strategy intelligence APS catalog — PHASE-5 SIP."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from athena_core.domain.strategy.builtin import builtin_strategy_registry

StrategyStatus = Literal["MVP", "Partial", "Deferred"]


@dataclass(frozen=True, slots=True)
class StrategyApsCatalogEntry:
    """APS spec entry for strategy intelligence platform."""

    aps_id: str
    name: str
    domain: str
    status: StrategyStatus


def _s(aps_id: str, name: str, domain: str, status: StrategyStatus = "Deferred") -> StrategyApsCatalogEntry:
    return StrategyApsCatalogEntry(aps_id, name, domain, status)


STRATEGY_APS_CATALOG: tuple[StrategyApsCatalogEntry, ...] = (
    _s("APS-STRAT-CORE-001", "Strategy Core", "Strategy-Framework", "MVP"),
    _s("APS-STRAT-REGISTRY-001", "Strategy Registry", "Strategy-Framework", "MVP"),
    _s("APS-STRAT-MANAGER-001", "Strategy Manager", "Strategy-Framework", "Partial"),
    _s("APS-STRAT-CONTEXT-001", "Strategy Context", "Strategy-Framework", "Partial"),
    _s("APS-STRAT-LIFECYCLE-001", "Strategy Lifecycle", "Strategy-Framework", "Deferred"),
    _s("APS-STRAT-STATE-001", "Strategy State", "Strategy-Framework", "Deferred"),
    _s("APS-STRAT-METADATA-001", "Strategy Metadata", "Strategy-Framework", "MVP"),
    _s("APS-STRAT-PIPELINE-001", "Strategy Decision Pipeline", "Strategy-Framework", "Partial"),
    _s("APS-SIGNAL-CORE-001", "Signal Object", "Signal-Framework", "MVP"),
    _s("APS-SIGNAL-CONFIDENCE-001", "Signal Confidence Engine", "Signal-Framework", "Deferred"),
    _s("APS-SIGNAL-SCORING-001", "Signal Scoring", "Signal-Framework", "Deferred"),
    _s("APS-SIGNAL-FILTER-001", "Signal Filter", "Signal-Framework", "Partial"),
    _s("APS-SIGNAL-RANK-001", "Signal Ranking", "Signal-Framework", "Deferred"),
    _s("APS-SIGNAL-DEDUP-001", "Duplicate Signal Filter", "Signal-Framework", "Deferred"),
    _s("APS-SIGNAL-EXPIRE-001", "Expired Signal Filter", "Signal-Framework", "Deferred"),
    _s("APS-SIGNAL-WEAK-001", "Weak Signal Filter", "Signal-Framework", "Deferred"),
    _s("APS-SIGNAL-BUY-001", "Buy Signal Qualification", "Signal-Framework", "Deferred"),
    _s("APS-SIGNAL-SELL-001", "Sell Signal Qualification", "Signal-Framework", "Deferred"),
    _s("APS-SIGNAL-STRENGTH-001", "Signal Strength", "Signal-Framework", "Deferred"),
    _s("APS-SIGNAL-REASON-001", "Signal Reason Codes", "Signal-Framework", "Deferred"),
    _s("APS-ENTRY-LONG-001", "Long Entries", "Entry-Engine", "MVP"),
    _s("APS-ENTRY-SHORT-001", "Short Entries", "Entry-Engine", "Deferred"),
    _s("APS-ENTRY-CONFIRM-001", "Entry Confirmation", "Entry-Engine", "Deferred"),
    _s("APS-ENTRY-TIMING-001", "Entry Timing", "Entry-Engine", "Deferred"),
    _s("APS-ENTRY-IMMEDIATE-001", "Immediate Entry", "Entry-Engine", "Deferred"),
    _s("APS-ENTRY-NEXTCANDLE-001", "Next Candle Entry", "Entry-Engine", "Deferred"),
    _s("APS-ENTRY-LIMIT-001", "Limit Entry", "Entry-Engine", "Deferred"),
    _s("APS-ENTRY-STOP-001", "Stop Entry", "Entry-Engine", "Deferred"),
    _s("APS-ENTRY-PULLBACK-001", "Pullback Entry", "Entry-Engine", "MVP"),
    _s("APS-ENTRY-BREAKOUT-001", "Breakout Entry", "Entry-Engine", "Deferred"),
    _s("APS-EXIT-STOPLOSS-001", "Stop Loss Exit", "Exit-Engine", "MVP"),
    _s("APS-EXIT-TAKEPROFIT-001", "Take Profit Exit", "Exit-Engine", "MVP"),
    _s("APS-EXIT-TIME-001", "Time Based Exit", "Exit-Engine", "Deferred"),
    _s("APS-EXIT-SIGNAL-001", "Signal Based Exit", "Exit-Engine", "MVP"),
    _s("APS-EXIT-SCALEOUT-001", "Scale Out Exit", "Exit-Engine", "Deferred"),
    _s("APS-EXIT-ATRSTOP-001", "ATR Stop Loss", "Exit-Engine", "Deferred"),
    _s("APS-EXIT-TRAILING-001", "Trailing Stop", "Exit-Engine", "Deferred"),
    _s("APS-EXIT-SWING-001", "Swing Stop", "Exit-Engine", "Deferred"),
    _s("APS-EXIT-RR-001", "Risk Reward Take Profit", "Exit-Engine", "Deferred"),
    _s("APS-EXIT-STRUCTURE-001", "Structure Based Exit", "Exit-Engine", "Deferred"),
    _s("APS-EXIT-VOLATILITY-001", "Volatility Exit", "Exit-Engine", "Deferred"),
    _s("APS-EXIT-INDICATOR-001", "Indicator Exit", "Exit-Engine", "Deferred"),
    _s("APS-RISK-PERTRADE-001", "Per Trade Risk", "Risk-Engine", "MVP"),
    _s("APS-RISK-DAILY-001", "Daily Stop", "Risk-Engine", "Deferred"),
    _s("APS-RISK-DRAWDOWN-001", "Maximum Drawdown", "Risk-Engine", "MVP"),
    _s("APS-RISK-CORRELATION-001", "Correlation Risk", "Risk-Engine", "Deferred"),
    _s("APS-RISK-SECTOR-001", "Sector Exposure Risk", "Risk-Engine", "Deferred"),
    _s("APS-RISK-EXPOSURE-001", "Net Gross Exposure", "Risk-Engine", "Partial"),
    _s("APS-RISK-POSITION-001", "Position Limit", "Risk-Engine", "Deferred"),
    _s("APS-RISK-VAR-001", "Value at Risk", "Risk-Engine", "Deferred"),
    _s("APS-RISK-VOLATILITY-001", "Volatility Risk", "Risk-Engine", "Deferred"),
    _s("APS-RISK-CONCENTRATION-001", "Concentration Risk", "Risk-Engine", "Deferred"),
    _s("APS-RISK-LEVERAGE-001", "Leverage Limit", "Risk-Engine", "Deferred"),
    _s("APS-RISK-MARGIN-001", "Margin Risk", "Risk-Engine", "Deferred"),
    _s("APS-RISK-SESSION-001", "Session Risk", "Risk-Engine", "Deferred"),
    _s("APS-RISK-EVENT-001", "Event Risk", "Risk-Engine", "Deferred"),
    _s("APS-RISK-PORTFOLIO-001", "Portfolio Risk Context", "Risk-Engine", "Deferred"),
    _s("APS-POS-FIXED-001", "Fixed Position Size", "Position-Sizing", "MVP"),
    _s("APS-POS-RISKPERCENT-001", "Risk Percent Sizing", "Position-Sizing", "MVP"),
    _s("APS-POS-ATR-001", "ATR Position Sizing", "Position-Sizing", "Deferred"),
    _s("APS-POS-KELLY-001", "Kelly Criterion Sizing", "Position-Sizing", "Deferred"),
    _s("APS-POS-VOLATILITY-001", "Volatility Sizing", "Position-Sizing", "Deferred"),
    _s("APS-POS-EQUALWEIGHT-001", "Equal Weight Sizing", "Position-Sizing", "Deferred"),
    _s("APS-POS-RISKPARITY-001", "Risk Parity Sizing", "Position-Sizing", "Deferred"),
    _s("APS-POS-FIXEDFRACTIONAL-001", "Fixed Fractional Sizing", "Position-Sizing", "Deferred"),
    _s("APS-POS-MAXPOSITION-001", "Max Position Cap", "Position-Sizing", "Deferred"),
    _s("APS-POS-SCALING-001", "Scaling In Out", "Position-Sizing", "Deferred"),
    _s("APS-POS-PORTFOLIO-001", "Portfolio Level Sizing", "Position-Sizing", "Deferred"),
    _s("APS-POS-DYNAMIC-001", "Dynamic Sizing", "Position-Sizing", "Deferred"),
    _s("APS-TEMPLATE-TREND-001", "Trend Following Template", "Strategy-Templates", "MVP"),
    _s("APS-TEMPLATE-MR-001", "Mean Reversion Template", "Strategy-Templates", "Deferred"),
    _s("APS-TEMPLATE-BREAKOUT-001", "Breakout Template", "Strategy-Templates", "Deferred"),
    _s("APS-TEMPLATE-MOMENTUM-001", "Momentum Template", "Strategy-Templates", "Deferred"),
    _s("APS-TEMPLATE-SCALPING-001", "Scalping Template", "Strategy-Templates", "Deferred"),
    _s("APS-TEMPLATE-SWING-001", "Swing Template", "Strategy-Templates", "Deferred"),
    _s("APS-TEMPLATE-EMA-001", "EMA Crossover Template", "Strategy-Templates", "MVP"),
    _s("APS-TEMPLATE-RSI-001", "RSI Template", "Strategy-Templates", "Deferred"),
    _s("APS-TEMPLATE-MACD-001", "MACD Template", "Strategy-Templates", "Deferred"),
    _s("APS-TEMPLATE-BOLLINGER-001", "Bollinger Template", "Strategy-Templates", "Deferred"),
    _s("APS-TEMPLATE-DONCHIAN-001", "Donchian Template", "Strategy-Templates", "Deferred"),
    _s("APS-TEMPLATE-PULLBACK-001", "Pullback Template", "Strategy-Templates", "MVP"),
    _s("APS-TEMPLATE-PAIRS-001", "Pairs Trading Template", "Strategy-Templates", "Deferred"),
    _s("APS-TEMPLATE-GRID-001", "Grid Template", "Strategy-Templates", "Deferred"),
    _s("APS-TEMPLATE-DCA-001", "DCA Template", "Strategy-Templates", "Deferred"),
    _s("APS-TEMPLATE-SECTORROT-001", "Sector Rotation Template", "Strategy-Templates", "Deferred"),
    _s("APS-TEMPLATE-VOLATILITY-001", "Volatility Template", "Strategy-Templates", "Deferred"),
    _s("APS-TEMPLATE-SEASONAL-001", "Seasonal Template", "Strategy-Templates", "Deferred"),
    _s("APS-TEMPLATE-EVENT-001", "Event Driven Template", "Strategy-Templates", "Deferred"),
    _s("APS-TEMPLATE-CUSTOM-001", "Custom DSL Template", "Strategy-Templates", "Deferred"),
    _s("APS-MTF-CONTEXT-001", "Higher Timeframe Context", "Multi-Timeframe", "Deferred"),
    _s("APS-MTF-CONFIRM-001", "Lower Timeframe Confirmation", "Multi-Timeframe", "Deferred"),
    _s("APS-MTF-SYNC-001", "Timeframe Synchronization", "Multi-Timeframe", "Deferred"),
    _s("APS-MTF-BIAS-001", "Timeframe Bias", "Multi-Timeframe", "Deferred"),
    _s("APS-MTF-ALIGN-001", "Timeframe Alignment", "Multi-Timeframe", "Deferred"),
    _s("APS-MTF-DIVERGE-001", "Timeframe Divergence", "Multi-Timeframe", "Deferred"),
    _s("APS-MTF-RESAMPLE-001", "Bar Resampling", "Multi-Timeframe", "Deferred"),
    _s("APS-MTF-FILTER-001", "MTF Signal Filter", "Multi-Timeframe", "Deferred"),
    _s("APS-COMP-AND-001", "AND Composition", "Strategy-Composition", "MVP"),
    _s("APS-COMP-OR-001", "OR Composition", "Strategy-Composition", "MVP"),
    _s("APS-COMP-NOT-001", "NOT Composition", "Strategy-Composition", "Deferred"),
    _s("APS-COMP-WEIGHTED-001", "Weighted Composition", "Strategy-Composition", "MVP"),
    _s("APS-COMP-VOTING-001", "Voting Composition", "Strategy-Composition", "MVP"),
    _s("APS-COMP-THRESHOLD-001", "Threshold Composition", "Strategy-Composition", "Deferred"),
    _s("APS-COMP-SEQUENCE-001", "Sequence Composition", "Strategy-Composition", "Deferred"),
    _s("APS-COMP-NESTED-001", "Nested Composition", "Strategy-Composition", "Deferred"),
    _s("APS-COMP-OVERRIDE-001", "Override Composition", "Strategy-Composition", "Deferred"),
    _s("APS-COMP-CONFLICT-001", "Conflict Resolution", "Strategy-Composition", "Deferred"),
    _s("APS-DSL-PARSER-001", "DSL Parser", "Strategy-DSL", "Deferred"),
    _s("APS-DSL-COMPILER-001", "DSL Compiler", "Strategy-DSL", "Deferred"),
    _s("APS-DSL-VALIDATOR-001", "DSL Validator", "Strategy-DSL", "Partial"),
    _s("APS-DSL-EXECUTOR-001", "DSL Executor", "Strategy-DSL", "Partial"),
    _s("APS-DSL-ENTRY-001", "DSL Entry Rules", "Strategy-DSL", "Deferred"),
    _s("APS-DSL-EXIT-001", "DSL Exit Rules", "Strategy-DSL", "Deferred"),
    _s("APS-DSL-RISK-001", "DSL Risk Block", "Strategy-DSL", "Deferred"),
    _s("APS-DSL-INDICATOR-001", "DSL Indicator References", "Strategy-DSL", "Deferred"),
    _s("APS-DSL-PATTERN-001", "DSL Pattern References", "Strategy-DSL", "Deferred"),
    _s("APS-DSL-UNIVERSE-001", "DSL Universe Block", "Strategy-DSL", "Deferred"),
    _s("APS-DSL-VERSION-001", "DSL Versioning", "Strategy-DSL", "Deferred"),
    _s("APS-DSL-IMPORT-001", "DSL Import", "Strategy-DSL", "Deferred"),
    _s("APS-OPT-GRID-001", "Grid Search Optimizer", "Strategy-Optimizer", "Deferred"),
    _s("APS-OPT-RANDOM-001", "Random Search Optimizer", "Strategy-Optimizer", "Deferred"),
    _s("APS-OPT-BAYESIAN-001", "Bayesian Optimizer", "Strategy-Optimizer", "Deferred"),
    _s("APS-OPT-GENETIC-001", "Genetic Algorithm Optimizer", "Strategy-Optimizer", "Deferred"),
    _s("APS-OPT-PSO-001", "Particle Swarm Optimizer", "Strategy-Optimizer", "Deferred"),
    _s("APS-OPT-WALKFORWARD-001", "Walk Forward Optimizer", "Strategy-Optimizer", "Deferred"),
    _s("APS-OPT-OBJECTIVE-001", "Objective Function", "Strategy-Optimizer", "Deferred"),
    _s("APS-OPT-CONSTRAINT-001", "Optimization Constraints", "Strategy-Optimizer", "Deferred"),
    _s("APS-OPT-PARAMSPACE-001", "Parameter Space", "Strategy-Optimizer", "Deferred"),
    _s("APS-OPT-RESULTS-001", "Optimization Results", "Strategy-Optimizer", "Deferred"),
    _s("APS-OPT-OVERFIT-001", "Overfit Detection", "Strategy-Optimizer", "Deferred"),
    _s("APS-OPT-STABILITY-001", "Parameter Stability", "Strategy-Optimizer", "Deferred"),
    _s("APS-OPT-SENSITIVITY-001", "Sensitivity Analysis", "Strategy-Optimizer", "Deferred"),
    _s("APS-OPT-ENSEMBLE-001", "Ensemble Optimization", "Strategy-Optimizer", "Deferred"),
    _s("APS-OPT-MULTIOBJ-001", "Multi Objective Optimization", "Strategy-Optimizer", "Deferred"),
    _s("APS-OPT-EARLYSTOP-001", "Early Stopping", "Strategy-Optimizer", "Deferred"),
    _s("APS-OPT-CROSSVAL-001", "Cross Validation", "Strategy-Optimizer", "Deferred"),
    _s("APS-OPT-REPORT-001", "Optimization Report", "Strategy-Optimizer", "Deferred"),
    _s("APS-OPT-PARALLEL-001", "Parallel Optimization", "Strategy-Optimizer", "Deferred"),
    _s("APS-OPT-CHECKPOINT-001", "Optimization Checkpoint", "Strategy-Optimizer", "Deferred"),
    _s("APS-STRAT-VAL-DEPS-001", "Missing Dependency Check", "Strategy-Validation", "MVP"),
    _s("APS-STRAT-VAL-IND-001", "Indicator Reference Validation", "Strategy-Validation", "MVP"),
    _s("APS-STRAT-VAL-CIRCULAR-001", "Circular Reference Check", "Strategy-Validation", "Deferred"),
    _s("APS-STRAT-VAL-DUP-001", "Duplicate Signal Check", "Strategy-Validation", "Deferred"),
    _s("APS-STRAT-VAL-LOOKAHEAD-001", "Lookahead Bias Check", "Strategy-Validation", "Deferred"),
    _s("APS-STRAT-VAL-LEAKAGE-001", "Data Leakage Check", "Strategy-Validation", "Deferred"),
    _s("APS-STRAT-VAL-SCHEMA-001", "Config Schema Validation", "Strategy-Validation", "MVP"),
    _s("APS-STRAT-VAL-UNIVERSE-001", "Universe Validation", "Strategy-Validation", "Deferred"),
    _s("APS-STRAT-VAL-RISK-001", "Risk Block Validation", "Strategy-Validation", "Deferred"),
    _s("APS-STRAT-VAL-EXPR-001", "Expression Validation", "Strategy-Validation", "Partial"),
    _s("APS-STRAT-REG-CORE-001", "Registry Core", "Strategy-Registry", "MVP"),
    _s("APS-STRAT-REG-VERSION-001", "Strategy Versioning", "Strategy-Registry", "Deferred"),
    _s("APS-STRAT-REG-ALIAS-001", "Strategy Aliases", "Strategy-Registry", "Deferred"),
    _s("APS-STRAT-REG-PERF-001", "Strategy Performance Metadata", "Strategy-Registry", "Deferred"),
    _s("APS-STRAT-REG-DEPS-001", "Strategy Dependencies", "Strategy-Registry", "Deferred"),
    _s("APS-STRAT-BENCH-LATENCY-001", "Signal Latency Benchmark", "Strategy-Benchmark", "Deferred"),
    _s("APS-STRAT-BENCH-MEMORY-001", "Memory Usage Benchmark", "Strategy-Benchmark", "Deferred"),
    _s("APS-STRAT-BENCH-THROUGHPUT-001", "Throughput Benchmark", "Strategy-Benchmark", "Deferred"),
    _s("APS-STRAT-BENCH-CPU-001", "CPU Usage Benchmark", "Strategy-Benchmark", "Deferred"),
    _s("APS-STRAT-BENCH-REPLAY-001", "Historical Replay Benchmark", "Strategy-Benchmark", "Deferred"),
    _s("APS-STRAT-TEST-UNIT-001", "Strategy Unit Tests", "Strategy-Testing", "Deferred"),
    _s("APS-STRAT-TEST-INTEGRATION-001", "Strategy Integration Tests", "Strategy-Testing", "Deferred"),
    _s("APS-STRAT-TEST-PROPERTY-001", "Property Based Tests", "Strategy-Testing", "Deferred"),
    _s("APS-STRAT-TEST-REPLAY-001", "Historical Replay Tests", "Strategy-Testing", "Deferred"),
    _s("APS-STRAT-TEST-GOLDEN-001", "Golden Dataset Tests", "Strategy-Testing", "Deferred"),
    _s("APS-STRAT-TEST-MONTECARLO-001", "Monte Carlo Verification", "Strategy-Testing", "Deferred"),
    _s("APS-STRAT-TEST-SIGNAL-001", "Signal Generation Tests", "Strategy-Testing", "Deferred"),
    _s("APS-STRAT-TEST-RISK-001", "Risk Qualification Tests", "Strategy-Testing", "Deferred"),
    _s("APS-STRAT-TEST-PIPELINE-001", "Pipeline Stage Tests", "Strategy-Testing", "Partial"),
    _s("APS-STRAT-TEST-COMPOSITION-001", "Composition Tests", "Strategy-Testing", "MVP"),
)


@dataclass(frozen=True, slots=True)
class StrategyCatalogEntry:
    """Metadata for a built-in strategy template."""

    strategy_id: str
    aps_id: str
    name: str
    status: StrategyStatus


_TEMPLATE_APS: dict[str, str] = {
    "ema_crossover": "APS-TEMPLATE-TREND-001",
    "ema_pullback": "APS-TEMPLATE-PULLBACK-001",
}


def build_strategy_catalog() -> tuple[StrategyCatalogEntry, ...]:
    """Build catalog from registered builtin strategies."""
    return tuple(
        StrategyCatalogEntry(
            strategy_id=strategy_id,
            aps_id=_TEMPLATE_APS.get(strategy_id, "APS-STRAT-REGISTRY-001"),
            name=config.strategy.description or strategy_id.replace("_", " ").title(),
            status="MVP",
        )
        for strategy_id, config in builtin_strategy_registry().items()
    )


STRATEGY_CATALOG: tuple[StrategyCatalogEntry, ...] = build_strategy_catalog()


def list_mvp_strategy_aps() -> list[StrategyApsCatalogEntry]:
    return [e for e in STRATEGY_APS_CATALOG if e.status == "MVP"]


def lookup_strategy_aps(strategy_id: str) -> StrategyCatalogEntry | None:
    """Resolve APS metadata for a strategy id."""
    for entry in STRATEGY_CATALOG:
        if entry.strategy_id == strategy_id:
            return entry
    return None


def lookup_strategy_aps_by_id(aps_id: str) -> StrategyApsCatalogEntry | None:
    """Resolve APS catalog entry by id."""
    for entry in STRATEGY_APS_CATALOG:
        if entry.aps_id == aps_id:
            return entry
    return None


"""Natural-language research intent models — REQ-AI-ASSISTANT-001."""

from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, Field


class WorkflowAction(StrEnum):
    """High-level workflow the assistant should run."""

    SCAN = "scan"
    BACKTEST = "backtest"
    WALK_FORWARD = "walk_forward"
    OPTIMIZE = "optimize"
    COMPARE = "compare"
    FULL_RESEARCH = "full_research"


class StrategyHint(StrEnum):
    """Strategy family inferred from user language."""

    EMA = "ema"
    SMA = "sma"
    CROSSOVER = "crossover"
    ANY = "any"


class MarketRegime(StrEnum):
    """Market regime filter inferred from user language."""

    SIDEWAYS = "sideways"
    TRENDING = "trending"
    VOLATILE = "volatile"
    ANY = "any"


class ResearchIntent(BaseModel):
    """Structured intent parsed from a natural-language query."""

    raw_query: str
    action: WorkflowAction = WorkflowAction.FULL_RESEARCH
    strategy_hint: StrategyHint = StrategyHint.ANY
    regime: MarketRegime = MarketRegime.ANY
    compare_latest: int | None = Field(
        default=None,
        description="When set, compare the N most recent experiments.",
    )
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)
    parser: str = Field(default="rule_based", description="Parser that produced this intent.")

"""Strategy decision pipeline — APS-STRAT-PIPELINE-001, SIP layered decisions."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from athena_core.domain.strategy.types import TradeSignal


class StrategyPipelineStage(str, Enum):
    """Ordered qualification layers from market data to trade decision."""

    INDICATORS = "indicators"
    PATTERNS = "patterns"
    MARKET_STRUCTURE = "market_structure"
    SIGNAL_GENERATION = "signal_generation"
    SIGNAL_QUALIFICATION = "signal_qualification"
    RISK_QUALIFICATION = "risk_qualification"
    PORTFOLIO_QUALIFICATION = "portfolio_qualification"
    EXECUTION_QUALIFICATION = "execution_qualification"
    TRADE_DECISION = "trade_decision"


@dataclass(frozen=True, slots=True)
class StrategyStageResult:
    """Output from a single decision layer."""

    stage: StrategyPipelineStage
    signals: tuple[TradeSignal, ...] = ()
    accepted: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)


class StrategyPipeline:
    """Layered strategy decision process per SIP architecture."""

    DEFAULT_STAGES: tuple[StrategyPipelineStage, ...] = tuple(StrategyPipelineStage)

    def __init__(
        self,
        *,
        stages: tuple[StrategyPipelineStage, ...] | None = None,
        min_confidence: float = 0.5,
    ) -> None:
        self._stages = stages or self.DEFAULT_STAGES
        self._min_confidence = min_confidence

    @property
    def stages(self) -> tuple[StrategyPipelineStage, ...]:
        return self._stages

    def run(self, signals: list[TradeSignal]) -> list[StrategyStageResult]:
        """Qualify signals through each decision layer."""
        results: list[StrategyStageResult] = []
        current = list(signals)

        for stage in self._stages:
            if stage == StrategyPipelineStage.SIGNAL_GENERATION:
                results.append(
                    StrategyStageResult(
                        stage=stage,
                        signals=tuple(current),
                        metadata={"input_count": len(current)},
                    )
                )
            elif stage == StrategyPipelineStage.SIGNAL_QUALIFICATION:
                current = [s for s in current if s.confidence >= self._min_confidence]
                results.append(
                    StrategyStageResult(
                        stage=stage,
                        signals=tuple(current),
                        metadata={"qualified_count": len(current)},
                    )
                )
            elif stage == StrategyPipelineStage.TRADE_DECISION:
                accepted = len(current) > 0
                results.append(
                    StrategyStageResult(stage=stage, signals=tuple(current), accepted=accepted)
                )
            else:
                results.append(
                    StrategyStageResult(
                        stage=stage,
                        signals=tuple(current),
                        metadata={"status": "deferred"},
                    )
                )

        return results

    def decide(self, signals: list[TradeSignal]) -> list[TradeSignal]:
        """Return signals that pass all qualification layers."""
        for result in reversed(self.run(signals)):
            if result.stage == StrategyPipelineStage.TRADE_DECISION and result.accepted:
                return list(result.signals)
        return []

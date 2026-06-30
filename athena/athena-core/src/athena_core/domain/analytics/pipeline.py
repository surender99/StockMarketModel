"""Quantitative service layer pipeline — PHASE 8 QARIP."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any

import pandas as pd

from athena_core.application.statistics_engine import PerformanceStatistics, StatisticsEngine
from athena_core.domain.analytics.risk import RiskReport, analyze_risk
from athena_core.domain.backtest import TradeRecord


class AnalyticsPipelineStage(str, Enum):
    """Ordered quantitative analytics layers."""

    DESCRIPTIVE = "descriptive"
    PERFORMANCE = "performance"
    RISK = "risk"
    FACTOR = "factor"
    REPORTING = "reporting"


@dataclass(frozen=True, slots=True)
class AnalyticsStageResult:
    """Output from a single analytics layer."""

    stage: AnalyticsPipelineStage
    completed: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class AnalyticsReport:
    """Consolidated quantitative analytics output."""

    performance: PerformanceStatistics | None = None
    risk: RiskReport | None = None
    stages: tuple[AnalyticsStageResult, ...] = ()


class AnalyticsPipeline:
    """Quantitative service layer — single entry for stats, risk, and reporting."""

    DEFAULT_STAGES: tuple[AnalyticsPipelineStage, ...] = (
        AnalyticsPipelineStage.DESCRIPTIVE,
        AnalyticsPipelineStage.PERFORMANCE,
        AnalyticsPipelineStage.RISK,
        AnalyticsPipelineStage.REPORTING,
    )

    def __init__(
        self,
        *,
        stages: tuple[AnalyticsPipelineStage, ...] | None = None,
        engine: StatisticsEngine | None = None,
    ) -> None:
        self._stages = stages or self.DEFAULT_STAGES
        self._engine = engine or StatisticsEngine()

    @property
    def stages(self) -> tuple[AnalyticsPipelineStage, ...]:
        return self._stages

    def run(
        self,
        equity_curve: pd.DataFrame,
        trades: list[TradeRecord],
        *,
        initial_capital: float,
        trading_days_per_year: int = 252,
    ) -> AnalyticsReport:
        """Execute configured analytics stages and return a consolidated report."""
        stage_results: list[AnalyticsStageResult] = []
        performance: PerformanceStatistics | None = None
        risk: RiskReport | None = None

        for stage in self._stages:
            if stage == AnalyticsPipelineStage.DESCRIPTIVE:
                stage_results.append(
                    AnalyticsStageResult(
                        stage=stage,
                        completed=not equity_curve.empty,
                        metadata={"rows": len(equity_curve)},
                    )
                )
            elif stage == AnalyticsPipelineStage.PERFORMANCE:
                performance = self._engine.compute_performance(
                    equity_curve,
                    trades,
                    initial_capital=initial_capital,
                    trading_days_per_year=trading_days_per_year,
                )
                stage_results.append(
                    AnalyticsStageResult(
                        stage=stage,
                        completed=True,
                        metadata={"trade_count": performance.trade_count},
                    )
                )
            elif stage == AnalyticsPipelineStage.RISK:
                risk = analyze_risk(equity_curve, trading_days_per_year=trading_days_per_year)
                stage_results.append(
                    AnalyticsStageResult(
                        stage=stage,
                        completed=True,
                        metadata={"max_drawdown": risk.metrics.max_drawdown},
                    )
                )
            elif stage == AnalyticsPipelineStage.REPORTING:
                stage_results.append(
                    AnalyticsStageResult(
                        stage=stage,
                        completed=performance is not None and risk is not None,
                        metadata={"has_performance": performance is not None, "has_risk": risk is not None},
                    )
                )

        return AnalyticsReport(
            performance=performance,
            risk=risk,
            stages=tuple(stage_results),
        )

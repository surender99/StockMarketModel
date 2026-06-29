"""AI Research Scientist orchestrator — ATH-REL-012, FR-012."""

from __future__ import annotations

from typing import Any

from athena_ai.application.orchestrator import ResearchOrchestrator
from athena_ai.domain.ai_modules import (
    AIReviewResult,
    DocumentationDraft,
    Hypothesis,
    ResearchPlanDraft,
    StrategyDesign,
    list_ai_modules,
)
from athena_ai.domain.intent import ResearchIntent
from athena_ai.domain.research_plan import ResearchPlan


class AIResearchScientist:
    """Orchestrate AI research modules — extends ResearchOrchestrator."""

    def __init__(self, orchestrator: ResearchOrchestrator) -> None:
        self._orchestrator = orchestrator

    @property
    def modules(self) -> dict[str, str]:
        return list_ai_modules()

    def plan(self, intent: ResearchIntent) -> ResearchPlanDraft:
        """AI Planner — REQ-AI-PLANNER-001."""
        plan: ResearchPlan = self._orchestrator.build_plan(intent)
        return ResearchPlanDraft(
            query=intent.raw_query,
            steps=[step.description for step in plan.steps],
            rationale=plan.rationale,
        )

    def generate_hypothesis(self, query: str) -> Hypothesis:
        """AI Hypothesis Generator — REQ-AI-HYPOTHESIS-001."""
        return Hypothesis(
            statement=f"If market conditions match '{query}', momentum strategies outperform",
            variables=["momentum", "volatility", "regime"],
            expected_outcome="positive risk-adjusted returns",
            confidence=0.6,
        )

    def design_strategy(self, hypothesis: Hypothesis) -> StrategyDesign:
        """AI Strategy Designer — REQ-AI-STRATEGY-001."""
        return StrategyDesign(
            name=f"strategy_{hypothesis.variables[0]}",
            entry_rules=[f"Enter when {hypothesis.variables[0]} > threshold"],
            exit_rules=["Exit on trailing stop or signal reversal"],
            parameters={"lookback": 20, "threshold": 0.5},
        )

    def generate_features(self, strategy: StrategyDesign) -> list[str]:
        """AI Feature Generator."""
        return [f"{strategy.name}_{p}" for p in strategy.parameters]

    def optimize_parameters(self, strategy: StrategyDesign) -> dict[str, Any]:
        """AI Optimizer stub."""
        return {k: v for k, v in strategy.parameters.items()}

    def review(self, outputs: dict[str, Any]) -> AIReviewResult:
        """AI Reviewer — REQ-AI-REVIEWER-001."""
        has_metrics = bool(outputs.get("metrics") or outputs.get("aggregate_metrics"))
        findings = ["Metrics present"] if has_metrics else ["Missing validation metrics"]
        return AIReviewResult(
            passed=has_metrics,
            findings=findings,
            severity="info" if has_metrics else "warning",
            recommendations=["Run walk-forward validation"] if not has_metrics else [],
        )

    def generate_docs(
        self,
        plan: ResearchPlanDraft,
        *,
        experiment_ids: list[str] | None = None,
    ) -> DocumentationDraft:
        """AI Documentation Generator — REQ-AI-DOCS-001."""
        return DocumentationDraft(
            title=f"Research: {plan.query}",
            sections={
                "summary": plan.rationale,
                "steps": "\n".join(f"- {s}" for s in plan.steps),
            },
            experiment_ids=experiment_ids or [],
        )

    def execute_research(self, intent: ResearchIntent, *, dry_run: bool = False):
        """Full AI research pipeline."""
        draft = self.plan(intent)
        hypothesis = self.generate_hypothesis(intent.raw_query)
        strategy = self.design_strategy(hypothesis)
        plan = self._orchestrator.build_plan(intent)
        result = self._orchestrator.execute(plan, dry_run=dry_run)
        review = self.review(result.step_outputs)
        docs = self.generate_docs(draft, experiment_ids=result.experiment_ids)
        return {
            "plan": draft,
            "hypothesis": hypothesis,
            "strategy": strategy,
            "result": result,
            "review": review,
            "documentation": docs,
        }

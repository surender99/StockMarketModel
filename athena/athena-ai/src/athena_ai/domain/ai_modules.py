"""AI research scientist modules — ATH-REL-012."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any


AI_MODULES: dict[str, str] = {
    "planner": "AI Planner — research workflow planning",
    "research_agent": "AI Research Agent — experiment orchestration",
    "hypothesis": "AI Hypothesis Generator",
    "strategy_designer": "AI Strategy Designer",
    "feature_generator": "AI Feature Generator",
    "optimizer": "AI Optimizer",
    "reviewer": "AI Reviewer",
    "docs": "AI Documentation Generator",
}


@dataclass
class ResearchPlanDraft:
    """AI-generated research plan."""

    query: str
    steps: list[str]
    rationale: str
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))


@dataclass
class Hypothesis:
    """Testable research hypothesis."""

    statement: str
    variables: list[str]
    expected_outcome: str
    confidence: float = 0.5


@dataclass
class StrategyDesign:
    """AI-proposed strategy design."""

    name: str
    entry_rules: list[str]
    exit_rules: list[str]
    parameters: dict[str, Any] = field(default_factory=dict)


@dataclass
class AIReviewResult:
    """AI review of research output."""

    passed: bool
    findings: list[str]
    severity: str = "info"
    recommendations: list[str] = field(default_factory=list)


@dataclass
class DocumentationDraft:
    """Generated research documentation."""

    title: str
    sections: dict[str, str]
    experiment_ids: list[str] = field(default_factory=list)


def list_ai_modules() -> dict[str, str]:
    return dict(AI_MODULES)

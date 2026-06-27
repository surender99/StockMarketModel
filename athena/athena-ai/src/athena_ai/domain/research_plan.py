"""Research plan and result models — REQ-AI-ASSISTANT-001."""

from __future__ import annotations

from datetime import date
from typing import Any

from pydantic import BaseModel, Field

from athena_ai.domain.intent import ResearchIntent, WorkflowAction


class ResearchStep(BaseModel):
    """Single orchestrated step in a research plan."""

    action: WorkflowAction
    description: str
    strategy_path: str | None = None
    start: date | None = None
    end: date | None = None
    as_of: date | None = None
    track_experiment: bool = False
    compare_latest: int | None = None


class ResearchPlan(BaseModel):
    """Proposed multi-step research workflow."""

    intent: ResearchIntent
    steps: list[ResearchStep]
    strategy_path: str
    rationale: str


class Recommendation(BaseModel):
    """Validated recommendation backed by experiment evidence."""

    summary: str
    experiment_ids: list[str] = Field(default_factory=list)
    metrics: dict[str, Any] = Field(default_factory=dict)
    validation_passed: bool = False


class ResearchResult(BaseModel):
    """Outcome of proposing or executing a research plan."""

    session_id: str
    query: str
    plan: ResearchPlan
    dry_run: bool
    steps_executed: list[str] = Field(default_factory=list)
    step_outputs: dict[str, Any] = Field(default_factory=dict)
    recommendations: list[Recommendation] = Field(default_factory=list)
    experiment_ids: list[str] = Field(default_factory=list)

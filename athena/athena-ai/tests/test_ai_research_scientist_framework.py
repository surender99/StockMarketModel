"""AI research scientist framework tests — ATH-REL-012."""

from __future__ import annotations

from athena_ai.application.ai_scientist import AIResearchScientist
from athena_ai.application.orchestrator import ResearchOrchestrator
from athena_ai.domain.ai_modules import list_ai_modules
from athena_ai.domain.intent import ResearchIntent, WorkflowAction
from athena_ai.infrastructure.config import ResearchAssistantConfig
from athena_sdk import AthenaClient


def _scientist() -> AIResearchScientist:
    config = ResearchAssistantConfig()
    client = AthenaClient()
    orch = ResearchOrchestrator(client, config)
    return AIResearchScientist(orch)


def test_req_ai_planner_001_plan() -> None:
    """REQ-AI-PLANNER-001 — AI planner."""
    scientist = _scientist()
    intent = ResearchIntent(raw_query="momentum scan", action=WorkflowAction.SCAN)
    draft = scientist.plan(intent)
    assert draft.query == "momentum scan"
    assert len(draft.steps) >= 1


def test_req_ai_hypothesis_001_generator() -> None:
    """REQ-AI-HYPOTHESIS-001 — hypothesis generator."""
    scientist = _scientist()
    hyp = scientist.generate_hypothesis("trend following")
    assert "momentum" in hyp.variables
    assert hyp.statement


def test_req_ai_strategy_001_designer() -> None:
    """REQ-AI-STRATEGY-001 — strategy designer."""
    scientist = _scientist()
    hyp = scientist.generate_hypothesis("breakout")
    design = scientist.design_strategy(hyp)
    assert design.entry_rules
    assert design.parameters


def test_req_ai_reviewer_001_review() -> None:
    """REQ-AI-REVIEWER-001 — AI reviewer."""
    scientist = _scientist()
    passed = scientist.review({"metrics": {"sharpe": 1.2}})
    failed = scientist.review({})
    assert passed.passed
    assert not failed.passed


def test_req_ai_docs_001_documentation() -> None:
    """REQ-AI-DOCS-001 — documentation generator."""
    scientist = _scientist()
    intent = ResearchIntent(raw_query="test", action=WorkflowAction.BACKTEST)
    draft = scientist.plan(intent)
    docs = scientist.generate_docs(draft, experiment_ids=["exp-1"])
    assert docs.title
    assert "exp-1" in docs.experiment_ids


def test_ai_modules_registered() -> None:
    """FR-015 — AI modules list."""
    modules = list_ai_modules()
    assert "planner" in modules
    assert len(modules) >= 8


def test_ai_scientist_dry_run() -> None:
    """Full AI research pipeline dry-run."""
    scientist = _scientist()
    intent = ResearchIntent(raw_query="ema crossover", action=WorkflowAction.FULL_RESEARCH)
    output = scientist.execute_research(intent, dry_run=True)
    assert output["plan"]
    assert output["hypothesis"]
    assert output["documentation"]

"""Tests for ResearchAssistant facade — REQ-AI-ASSISTANT-001."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

from athena_ai.application.research_assistant import ResearchAssistant
from athena_ai.infrastructure.config import ResearchAssistantConfig


def test_propose_returns_plan(tmp_path: Path) -> None:
    config = ResearchAssistantConfig(
        default_strategy_path=str(tmp_path / "s.yaml"),
        ai_session_log_path=str(tmp_path / "ai"),
    )
    (tmp_path / "s.yaml").write_text("strategy:\n  id: x\n  version: '1'\n", encoding="utf-8")
    client = MagicMock()
    assistant = ResearchAssistant(client, research_config=config)
    plan = assistant.propose("scan ema stocks")
    assert plan.intent.action.value == "scan"
    assert plan.steps


def test_to_dict_serializes_result(tmp_path: Path) -> None:
    config = ResearchAssistantConfig(ai_session_log_path=str(tmp_path / "ai"))
    client = MagicMock()
    assistant = ResearchAssistant(client, research_config=config)
    with patch.object(assistant, "propose") as propose_mock:
        from athena_ai.application.intent_parser import RuleBasedIntentParser
        from athena_ai.application.orchestrator import ResearchOrchestrator

        intent = RuleBasedIntentParser().parse("compare latest 2")
        orchestrator = ResearchOrchestrator(client, config)
        plan = orchestrator.build_plan(intent)
        propose_mock.return_value = plan
        result = assistant.research("compare latest 2", dry_run=True)
    payload = assistant.to_dict(result)
    assert payload["query"] == "compare latest 2"
    assert "plan" in payload
    assert payload["dry_run"] is True

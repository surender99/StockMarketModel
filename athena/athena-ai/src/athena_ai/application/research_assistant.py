"""Research assistant facade — REQ-AI-ASSISTANT-001."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import structlog
from athena_sdk import AthenaClient

from athena_ai.application.intent_parser import parse_intent
from athena_ai.application.orchestrator import ResearchOrchestrator
from athena_ai.domain.research_plan import ResearchPlan, ResearchResult
from athena_ai.infrastructure.config import ResearchAssistantConfig, load_research_config

log = structlog.get_logger(__name__)


class ResearchAssistant:
    """Natural-language experiment orchestration atop AthenaClient — REQ-AI-ASSISTANT-001."""

    def __init__(
        self,
        client: AthenaClient | None = None,
        *,
        config_path: Path | str | None = None,
        research_config: ResearchAssistantConfig | None = None,
        profile: str | None = None,
        athena_config_path: Path | str | None = None,
    ) -> None:
        self._research_config = research_config or load_research_config(config_path)
        self._client = client or AthenaClient(
            config_path=athena_config_path or self._research_config.athena_config_path,
            profile=profile,
        )
        self._orchestrator = ResearchOrchestrator(self._client, self._research_config)

    @property
    def client(self) -> AthenaClient:
        return self._client

    @property
    def config(self) -> ResearchAssistantConfig:
        return self._research_config

    def propose(self, query: str, *, use_openai: bool | None = None) -> ResearchPlan:
        """Parse query and return an execution plan without running workflows."""
        intent = parse_intent(query, use_openai=self._resolve_openai(use_openai))
        log.info("research.intent_parsed", action=intent.action.value, parser=intent.parser)
        return self._orchestrator.build_plan(intent)

    def research(
        self,
        query: str,
        *,
        dry_run: bool = False,
        use_openai: bool | None = None,
    ) -> ResearchResult:
        """Parse query, build plan, and optionally execute via AthenaClient."""
        plan = self.propose(query, use_openai=use_openai)
        log.info(
            "research.execute",
            dry_run=dry_run,
            steps=len(plan.steps),
            strategy=plan.strategy_path,
        )
        return self._orchestrator.execute(plan, dry_run=dry_run)

    def to_dict(self, result: ResearchResult) -> dict[str, Any]:
        """Serialize result for CLI / JSON output."""
        return {
            "session_id": result.session_id,
            "query": result.query,
            "dry_run": result.dry_run,
            "plan": {
                "rationale": result.plan.rationale,
                "strategy_path": result.plan.strategy_path,
                "steps": [
                    {
                        "action": step.action.value,
                        "description": step.description,
                    }
                    for step in result.plan.steps
                ],
                "intent": {
                    "action": result.plan.intent.action.value,
                    "strategy_hint": result.plan.intent.strategy_hint.value,
                    "regime": result.plan.intent.regime.value,
                    "confidence": result.plan.intent.confidence,
                    "parser": result.plan.intent.parser,
                },
            },
            "steps_executed": result.steps_executed,
            "experiment_ids": result.experiment_ids,
            "recommendations": [
                {
                    "summary": rec.summary,
                    "experiment_ids": rec.experiment_ids,
                    "metrics": rec.metrics,
                    "validation_passed": rec.validation_passed,
                }
                for rec in result.recommendations
            ],
            "step_outputs": result.step_outputs,
        }

    def _resolve_openai(self, override: bool | None) -> bool:
        if override is not None:
            return override
        return self._research_config.use_openai_when_available

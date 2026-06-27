"""AI session experiment logging — REQ-AI-ASSISTANT-001."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

import structlog

from athena_ai.domain.research_plan import ResearchResult

log = structlog.get_logger(__name__)


class AIExperimentLogger:
    """Persist AI-proposed research sessions alongside core experiment tracking."""

    def __init__(self, base_path: str | Path) -> None:
        self._base = Path(base_path)

    def log_session(self, result: ResearchResult) -> Path:
        self._base.mkdir(parents=True, exist_ok=True)
        payload = {
            "session_id": result.session_id,
            "created_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
            "query": result.query,
            "dry_run": result.dry_run,
            "experiment_ids": result.experiment_ids,
            "steps_executed": result.steps_executed,
            "intent": {
                "action": result.plan.intent.action.value,
                "strategy_hint": result.plan.intent.strategy_hint.value,
                "regime": result.plan.intent.regime.value,
                "parser": result.plan.intent.parser,
            },
            "recommendations": [
                {
                    "summary": rec.summary,
                    "experiment_ids": rec.experiment_ids,
                    "validation_passed": rec.validation_passed,
                }
                for rec in result.recommendations
            ],
        }
        target = self._base / f"{result.session_id}.json"
        target.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        log.info("ai.session_logged", session_id=result.session_id, path=str(target))
        return target

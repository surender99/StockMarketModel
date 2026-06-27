"""Optional OpenAI-backed intent parser — REQ-AI-ASSISTANT-001."""

from __future__ import annotations

import json
import os
from typing import Any

import structlog

from athena_ai.application.intent_parser import RuleBasedIntentParser
from athena_ai.domain.intent import MarketRegime, ResearchIntent, StrategyHint, WorkflowAction
from athena_ai.infrastructure.config import ResearchAssistantConfig, load_research_config

log = structlog.get_logger(__name__)


class OpenAIIntentParser:
    """Delegates to OpenAI when API key is set; falls back to rules otherwise."""

    def __init__(self, config: ResearchAssistantConfig | None = None) -> None:
        self._config = config or load_research_config()
        self._fallback = RuleBasedIntentParser()
        self._api_key = os.environ.get("OPENAI_API_KEY")

    @property
    def available(self) -> bool:
        return bool(self._api_key)

    def parse(self, query: str) -> ResearchIntent:
        if not self.available:
            return self._fallback.parse(query)
        try:
            return self._parse_openai(query)
        except Exception as exc:  # noqa: BLE001 — graceful fallback for MVP
            log.warning("openai.parse_failed", error=str(exc))
            return self._fallback.parse(query)

    def _parse_openai(self, query: str) -> ResearchIntent:
        from openai import OpenAI

        client = OpenAI(api_key=self._api_key)
        system = (
            "Extract Athena research intent as JSON with keys: "
            "action (scan|backtest|walk_forward|optimize|compare|full_research), "
            "strategy_hint (ema|sma|crossover|any), regime (sideways|trending|volatile|any), "
            "compare_latest (int or null)."
        )
        response = client.chat.completions.create(
            model=self._config.openai_model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": query},
            ],
            response_format={"type": "json_object"},
            temperature=0,
        )
        content = response.choices[0].message.content or "{}"
        data: dict[str, Any] = json.loads(content)
        return ResearchIntent(
            raw_query=query,
            action=WorkflowAction(data.get("action", "full_research")),
            strategy_hint=StrategyHint(data.get("strategy_hint", "any")),
            regime=MarketRegime(data.get("regime", "any")),
            compare_latest=data.get("compare_latest"),
            confidence=0.85,
            parser="openai",
        )

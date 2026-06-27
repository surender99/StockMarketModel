"""Rule-based natural-language intent parser — REQ-AI-ASSISTANT-001."""

from __future__ import annotations

import re
from typing import Protocol

from athena_ai.domain.intent import MarketRegime, ResearchIntent, StrategyHint, WorkflowAction


class IntentParser(Protocol):
    """Port for parsing natural-language research queries."""

    def parse(self, query: str) -> ResearchIntent: ...


class RuleBasedIntentParser:
    """Keyword and pattern matcher for research intents — REQ-AI-ASSISTANT-001."""

    _ACTION_PATTERNS: list[tuple[re.Pattern[str], WorkflowAction]] = [
        (re.compile(r"\b(compare|comparison|rank)\b.*\bexperiment", re.I), WorkflowAction.COMPARE),
        (re.compile(r"\bcompare\b", re.I), WorkflowAction.COMPARE),
        (re.compile(r"\b(scan|screener|screen)\b", re.I), WorkflowAction.SCAN),
        (re.compile(r"\b(backtest|back\s*test)\b", re.I), WorkflowAction.BACKTEST),
        (re.compile(r"\b(walk[- ]?forward|out[- ]?of[- ]?sample|oos)\b", re.I), WorkflowAction.WALK_FORWARD),
        (re.compile(r"\b(optimize|optimi[sz]e|tune|grid\s*search)\b", re.I), WorkflowAction.OPTIMIZE),
        (
            re.compile(r"\b(find|discover|best|recommend|suggest|top)\b", re.I),
            WorkflowAction.FULL_RESEARCH,
        ),
    ]

    _STRATEGY_PATTERNS: list[tuple[re.Pattern[str], StrategyHint]] = [
        (re.compile(r"\bema\b", re.I), StrategyHint.EMA),
        (re.compile(r"\bsma\b", re.I), StrategyHint.SMA),
        (re.compile(r"\bcrossover\b", re.I), StrategyHint.CROSSOVER),
    ]

    _REGIME_PATTERNS: list[tuple[re.Pattern[str], MarketRegime]] = [
        (re.compile(r"\b(sideways|ranging|range[- ]?bound|choppy|consolidat)", re.I), MarketRegime.SIDEWAYS),
        (re.compile(r"\b(trending|trend|bull|bear|momentum)\b", re.I), MarketRegime.TRENDING),
        (re.compile(r"\b(volatile|volatility|high\s*vol)\b", re.I), MarketRegime.VOLATILE),
    ]

    def parse(self, query: str) -> ResearchIntent:
        text = query.strip()
        action = self._detect_action(text)
        strategy_hint = self._detect_strategy(text)
        regime = self._detect_regime(text)
        compare_latest = self._detect_compare_latest(text) if action == WorkflowAction.COMPARE else None
        if action == WorkflowAction.FULL_RESEARCH and compare_latest is None:
            compare_latest = 3
        confidence = self._score_confidence(text, action, strategy_hint, regime)
        return ResearchIntent(
            raw_query=text,
            action=action,
            strategy_hint=strategy_hint,
            regime=regime,
            compare_latest=compare_latest,
            confidence=confidence,
            parser="rule_based",
        )

    def _detect_action(self, text: str) -> WorkflowAction:
        for pattern, action in self._ACTION_PATTERNS:
            if pattern.search(text):
                return action
        return WorkflowAction.FULL_RESEARCH

    def _detect_strategy(self, text: str) -> StrategyHint:
        for pattern, hint in self._STRATEGY_PATTERNS:
            if pattern.search(text):
                return hint
        return StrategyHint.ANY

    def _detect_regime(self, text: str) -> MarketRegime:
        for pattern, regime in self._REGIME_PATTERNS:
            if pattern.search(text):
                return regime
        return MarketRegime.ANY

    @staticmethod
    def _detect_compare_latest(text: str) -> int | None:
        match = re.search(r"\b(?:latest|last|recent)\s+(\d+)\b", text, re.I)
        if match:
            return max(1, int(match.group(1)))
        if re.search(r"\b(latest|recent)\b", text, re.I):
            return 3
        return None

    @staticmethod
    def _score_confidence(
        text: str,
        action: WorkflowAction,
        strategy_hint: StrategyHint,
        regime: MarketRegime,
    ) -> float:
        score = 0.5
        if len(text.split()) >= 4:
            score += 0.1
        if action != WorkflowAction.FULL_RESEARCH:
            score += 0.15
        if strategy_hint != StrategyHint.ANY:
            score += 0.15
        if regime != MarketRegime.ANY:
            score += 0.1
        return min(1.0, score)


def parse_intent(query: str, *, use_openai: bool = False) -> ResearchIntent:
    """Parse query with optional OpenAI backend when configured."""
    if use_openai:
        from athena_ai.infrastructure.openai_parser import OpenAIIntentParser

        parser = OpenAIIntentParser()
        if parser.available:
            return parser.parse(query)
    return RuleBasedIntentParser().parse(query)

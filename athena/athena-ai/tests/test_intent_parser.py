"""Tests for rule-based intent parser — REQ-AI-ASSISTANT-001."""

from __future__ import annotations

from athena_ai.application.intent_parser import RuleBasedIntentParser
from athena_ai.domain.intent import MarketRegime, StrategyHint, WorkflowAction


def test_parse_full_research_ema_sideways() -> None:
    parser = RuleBasedIntentParser()
    intent = parser.parse("Find the best EMA strategy for sideways markets")
    assert intent.action == WorkflowAction.FULL_RESEARCH
    assert intent.strategy_hint == StrategyHint.EMA
    assert intent.regime == MarketRegime.SIDEWAYS
    assert intent.compare_latest == 3


def test_parse_scan_command() -> None:
    parser = RuleBasedIntentParser()
    intent = parser.parse("scan nifty500 for crossover signals")
    assert intent.action == WorkflowAction.SCAN
    assert intent.strategy_hint == StrategyHint.CROSSOVER


def test_parse_walk_forward() -> None:
    parser = RuleBasedIntentParser()
    intent = parser.parse("walk-forward validate sma strategy in volatile markets")
    assert intent.action == WorkflowAction.WALK_FORWARD
    assert intent.strategy_hint == StrategyHint.SMA
    assert intent.regime == MarketRegime.VOLATILE


def test_parse_compare_latest() -> None:
    parser = RuleBasedIntentParser()
    intent = parser.parse("compare latest 5 experiments")
    assert intent.action == WorkflowAction.COMPARE
    assert intent.compare_latest == 5


def test_parse_optimize() -> None:
    parser = RuleBasedIntentParser()
    intent = parser.parse("optimize ema parameters")
    assert intent.action == WorkflowAction.OPTIMIZE
    assert intent.strategy_hint == StrategyHint.EMA

"""Strategy configuration validation — ATH-REL-006 §5.10, FR-004–FR-008."""

from __future__ import annotations

import ast
import re

from athena_core.domain.strategy.config import StrategyConfig
from athena_core.domain.strategy.indicators import INDICATOR_TYPES, validate_indicator_specs


class StrategyValidationError(ValueError):
    """Strategy configuration failed validation."""


def _referenced_names(condition: str) -> set[str]:
    tree = ast.parse(condition, mode="eval")
    return {node.id for node in ast.walk(tree) if isinstance(node, ast.Name)}


def validate_strategy(strategy: StrategyConfig) -> list[str]:
    """Return validation issues for a strategy config (empty if valid)."""
    issues: list[str] = []

    try:
        validate_indicator_specs(strategy.indicators)
    except ValueError as exc:
        issues.append(str(exc))

    declared = strategy.indicator_ids()
    builtins = {"close", "volume"}
    for rule in strategy.entry.rules:
        refs = _referenced_names(rule.condition) - builtins
        missing = refs - declared
        if missing:
            issues.append(f"entry rule references unknown indicators: {sorted(missing)}")
    for rule in strategy.exit.rules:
        refs = _referenced_names(rule.condition) - builtins
        missing = refs - declared
        if missing:
            issues.append(f"exit rule references unknown indicators: {sorted(missing)}")

    entry_sides = [r.side for r in strategy.entry.rules]
    if len(entry_sides) != len(set(entry_sides)):
        issues.append("duplicate entry rule sides may conflict")

    if strategy.risk.stop_loss_pct is not None and strategy.risk.take_profit_pct is not None:
        if strategy.risk.stop_loss_pct >= strategy.risk.take_profit_pct:
            issues.append("stop_loss_pct should be less than take_profit_pct")

    for spec in strategy.indicators:
        if spec.type not in INDICATOR_TYPES:
            issues.append(f"unknown indicator type: {spec.type}")

    if re.search(r"shift\(\s*-\d+", " ".join(r.condition for r in strategy.entry.rules)):
        issues.append("negative shift lag implies lookahead")

    return issues


def validate_strategy_or_raise(strategy: StrategyConfig) -> None:
    """Validate strategy config; raise StrategyValidationError on failure."""
    issues = validate_strategy(strategy)
    if issues:
        raise StrategyValidationError("; ".join(issues))

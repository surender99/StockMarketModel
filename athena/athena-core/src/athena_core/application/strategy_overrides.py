"""Apply dot-path overrides to strategy configs — REQ-OPT-001."""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from athena_core.domain.strategy.config import StrategyConfig


def apply_strategy_overrides(
    strategy: StrategyConfig,
    overrides: dict[str, Any],
) -> StrategyConfig:
    """Return a new StrategyConfig with dot-path parameter overrides applied."""
    data = deepcopy(strategy.model_dump(mode="python"))
    for path, value in overrides.items():
        _set_nested_value(data, path, value)
    return StrategyConfig.model_validate(data)


def _set_nested_value(data: dict[str, Any], path: str, value: Any) -> None:
    parts = path.split(".")
    if len(parts) < 2:
        msg = f"invalid override path: {path}"
        raise ValueError(msg)

    if parts[0] == "indicators" and len(parts) >= 3:
        indicator_id = parts[1]
        remainder = parts[2:]
        indicators = data.get("indicators", [])
        for indicator in indicators:
            if indicator.get("id") == indicator_id:
                _assign_path(indicator, remainder, value)
                return
        msg = f"indicator id not found for override: {indicator_id}"
        raise ValueError(msg)

    _assign_path(data, parts, value)


def _assign_path(obj: dict[str, Any], parts: list[str], value: Any) -> None:
    cursor: dict[str, Any] = obj
    for part in parts[:-1]:
        if part not in cursor or not isinstance(cursor[part], dict):
            msg = f"invalid override path segment: {part}"
            raise ValueError(msg)
        cursor = cursor[part]
    cursor[parts[-1]] = value

"""YAML strategy loader — REQ-STRAT-CONFIG-001."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from pydantic import ValidationError

from athena_core.domain.strategy.config import StrategyConfig
from athena_core.domain.strategy.indicators import validate_indicator_specs


class StrategyLoadError(Exception):
    """Strategy YAML parse or validation failure."""

    def __init__(self, path: Path | None, message: str, field_path: str | None = None) -> None:
        self.path = path
        self.field_path = field_path
        location = f" ({field_path})" if field_path else ""
        src = f"{path}: " if path else ""
        super().__init__(f"{src}{message}{location}")


def load_strategy_yaml(path: Path | str) -> StrategyConfig:
    """Load and validate a strategy YAML file."""
    file_path = Path(path)
    if not file_path.is_file():
        raise StrategyLoadError(file_path, "strategy file not found")

    try:
        raw = yaml.safe_load(file_path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise StrategyLoadError(file_path, f"invalid YAML: {exc}") from exc

    if not isinstance(raw, dict):
        raise StrategyLoadError(file_path, "strategy root must be a mapping")

    try:
        config = StrategyConfig.model_validate(raw)
    except ValidationError as exc:
        first = exc.errors()[0]
        loc = ".".join(str(part) for part in first["loc"])
        raise StrategyLoadError(file_path, str(first["msg"]), field_path=loc) from exc

    try:
        validate_indicator_specs(config.indicators)
    except ValueError as exc:
        raise StrategyLoadError(file_path, str(exc)) from exc

    return config


def strategy_to_yaml(config: StrategyConfig) -> str:
    """Serialize strategy config to YAML for round-trip tests."""
    payload: dict[str, Any] = config.model_dump(mode="json")
    return yaml.safe_dump(payload, sort_keys=False)

"""Configuration loading — APS-001."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel

from athena_os.errors import ConfigurationError


class ConfigurationManager:
    """Load and validate configuration from YAML/JSON files."""

    def __init__(self, base_path: Path | None = None) -> None:
        self.base_path = base_path or Path(".")

    def load_file(self, path: Path | str) -> dict[str, Any]:
        resolved = Path(path)
        if not resolved.is_absolute():
            resolved = self.base_path / resolved
        if not resolved.exists():
            msg = f"configuration file not found: {resolved}"
            raise ConfigurationError(msg, context={"path": str(resolved)})
        text = resolved.read_text(encoding="utf-8")
        return self.loads(text, suffix=resolved.suffix)

    def loads(self, text: str, *, suffix: str = ".yaml") -> dict[str, Any]:
        if suffix in {".yaml", ".yml"}:
            data = yaml.safe_load(text)
        elif suffix == ".json":
            data = json.loads(text)
        else:
            msg = f"unsupported configuration format: {suffix}"
            raise ConfigurationError(msg, context={"suffix": suffix})
        if not isinstance(data, dict):
            msg = "configuration root must be a mapping"
            raise ConfigurationError(msg)
        return data

    def load_model(self, path: Path | str, model: type[BaseModel]) -> BaseModel:
        return model.model_validate(self.load_file(path))

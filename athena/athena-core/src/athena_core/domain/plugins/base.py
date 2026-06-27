"""Plugin base types — AES-0202."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class PluginType(str, Enum):
    """Registered plugin categories."""

    INDICATOR = "indicator"
    PATTERN = "pattern"
    STRATEGY = "strategy"
    RISK = "risk"
    REPORT = "report"
    ML_MODEL = "ml_model"


@dataclass(frozen=True)
class PluginMetadata:
    """Human-readable plugin identity."""

    name: str
    description: str = ""
    author: str = ""


@dataclass
class Plugin:
    """Minimal plugin contract — AES-0202."""

    id: str
    version: str
    plugin_type: PluginType
    metadata: PluginMetadata
    configuration_schema: dict[str, Any] = field(default_factory=dict)
    execute: Callable[..., Any] | None = None

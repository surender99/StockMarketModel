"""Plugin base types — AES-0202, ATH-REL-001 §03."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any


class PluginType(StrEnum):
    """Registered plugin categories."""

    INDICATOR = "indicator"
    PATTERN = "pattern"
    STRATEGY = "strategy"
    RISK = "risk"
    REPORT = "report"
    ML_MODEL = "ml_model"


class PluginLifecycle(StrEnum):
    """Plugin registration lifecycle states."""

    REGISTERED = "registered"
    ACTIVE = "active"
    DISABLED = "disabled"


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
    lifecycle: PluginLifecycle = PluginLifecycle.REGISTERED

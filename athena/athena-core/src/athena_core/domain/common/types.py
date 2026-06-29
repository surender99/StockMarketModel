"""Shared domain value types — ATH-REL-001 §07-Core-Utilities."""

from __future__ import annotations

import re
from dataclasses import dataclass

_VERSION_PATTERN = re.compile(r"^\d+\.\d+\.\d+$")


@dataclass(frozen=True, slots=True)
class Identifier:
    """Stable string identifier for plugins, services, and events."""

    value: str

    def __post_init__(self) -> None:
        if not self.value or not self.value.strip():
            msg = "identifier value must be non-empty"
            raise ValueError(msg)

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True)
class SemanticVersion:
    """Semantic version string (major.minor.patch)."""

    value: str

    def __post_init__(self) -> None:
        if not _VERSION_PATTERN.match(self.value):
            msg = f"invalid semantic version: {self.value!r}"
            raise ValueError(msg)

    def __str__(self) -> str:
        return self.value

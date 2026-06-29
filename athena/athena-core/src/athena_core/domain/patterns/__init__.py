"""Pattern recognition — AES-0600, ATH-REL-005."""

from athena_core.domain.patterns.base import PatternDetector, builtin_pattern_registry
from athena_core.domain.patterns.pattern_plugins import (
    register_builtin_patterns,
    resolve_pattern,
)
from athena_core.domain.patterns.types import PatternEvent, PatternType

__all__ = [
    "PatternDetector",
    "PatternEvent",
    "PatternType",
    "builtin_pattern_registry",
    "register_builtin_patterns",
    "resolve_pattern",
]

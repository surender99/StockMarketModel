"""Core error hierarchy — ATH-REL-001 §06-Error-Handling."""

from __future__ import annotations

from enum import StrEnum


class ErrorCode(StrEnum):
    """Stable error codes for Athena core failures."""

    CONFIGURATION = "ATH-CFG-001"
    VALIDATION = "ATH-VAL-001"
    NOT_FOUND = "ATH-NF-001"
    PLUGIN = "ATH-PLG-001"
    EVENT = "ATH-EVT-001"
    INGEST = "ATH-ING-001"
    INTERNAL = "ATH-INT-001"


class AthenaError(Exception):
    """Base exception with structured code and optional context."""

    def __init__(
        self,
        message: str,
        *,
        code: ErrorCode = ErrorCode.INTERNAL,
        context: dict[str, object] | None = None,
    ) -> None:
        self.code = code
        self.context = context or {}
        super().__init__(message)

    def __str__(self) -> str:
        base = f"[{self.code}] {super().__str__()}"
        if self.context:
            details = ", ".join(f"{key}={value!r}" for key, value in self.context.items())
            return f"{base} ({details})"
        return base


class ConfigurationError(AthenaError):
    """Invalid or missing configuration."""

    def __init__(self, message: str, *, context: dict[str, object] | None = None) -> None:
        super().__init__(message, code=ErrorCode.CONFIGURATION, context=context)


class ValidationError(AthenaError):
    """Input or domain validation failure."""

    def __init__(self, message: str, *, context: dict[str, object] | None = None) -> None:
        super().__init__(message, code=ErrorCode.VALIDATION, context=context)


class NotFoundError(AthenaError):
    """Requested resource does not exist."""

    def __init__(self, message: str, *, context: dict[str, object] | None = None) -> None:
        super().__init__(message, code=ErrorCode.NOT_FOUND, context=context)


class PluginError(AthenaError):
    """Plugin registration or execution failure."""

    def __init__(self, message: str, *, context: dict[str, object] | None = None) -> None:
        super().__init__(message, code=ErrorCode.PLUGIN, context=context)

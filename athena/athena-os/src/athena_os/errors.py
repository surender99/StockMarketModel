"""Infrastructure error hierarchy — ATH-REL-001 §06."""

from __future__ import annotations

from enum import StrEnum


class ErrorCode(StrEnum):
    CONFIGURATION = "ATH-CFG-001"
    VALIDATION = "ATH-VAL-001"
    NOT_FOUND = "ATH-NF-001"
    PLUGIN = "ATH-PLG-001"
    EVENT = "ATH-EVT-001"
    INTERNAL = "ATH-INT-001"


class AthenaOSError(Exception):
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


class ConfigurationError(AthenaOSError):
    def __init__(self, message: str, *, context: dict[str, object] | None = None) -> None:
        super().__init__(message, code=ErrorCode.CONFIGURATION, context=context)


class NotFoundError(AthenaOSError):
    def __init__(self, message: str, *, context: dict[str, object] | None = None) -> None:
        super().__init__(message, code=ErrorCode.NOT_FOUND, context=context)


class PluginError(AthenaOSError):
    def __init__(self, message: str, *, context: dict[str, object] | None = None) -> None:
        super().__init__(message, code=ErrorCode.PLUGIN, context=context)


class EventError(AthenaOSError):
    def __init__(self, message: str, *, context: dict[str, object] | None = None) -> None:
        super().__init__(message, code=ErrorCode.EVENT, context=context)

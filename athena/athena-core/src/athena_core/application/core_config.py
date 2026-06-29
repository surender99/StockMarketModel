"""Core framework configuration — ATH-REL-001 §01-Configuration."""

from __future__ import annotations

from pydantic import BaseModel, Field


class LoggingConfig(BaseModel):
    """Structured logging settings."""

    level: str = "INFO"
    json_logs: bool = False
    correlation_id_header: str = "X-Correlation-ID"


class CoreFrameworkConfig(BaseModel):
    """Release-01 core framework settings."""

    logging: LoggingConfig = Field(default_factory=LoggingConfig)
    enable_event_bus: bool = True

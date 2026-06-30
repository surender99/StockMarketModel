"""Structured logging — delegates to athena-os."""

from athena_os.logging import (
    bind_correlation_id,
    clear_correlation_id,
    configure_logging,
    correlation_scope,
    get_correlation_id,
    get_logger,
)

__all__ = [
    "bind_correlation_id",
    "clear_correlation_id",
    "configure_logging",
    "correlation_scope",
    "get_correlation_id",
    "get_logger",
]

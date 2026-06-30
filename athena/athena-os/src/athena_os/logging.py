"""Structured logging — ATH-REL-001 §05."""

from __future__ import annotations

import logging
import sys
import uuid
from contextlib import contextmanager
from contextvars import ContextVar, Token
from typing import Any, Iterator, cast

import structlog

_CORRELATION_ID: ContextVar[str | None] = ContextVar("athena_correlation_id", default=None)


def bind_correlation_id(correlation_id: str | None = None) -> str:
    value = correlation_id or uuid.uuid4().hex
    _CORRELATION_ID.set(value)
    structlog.contextvars.bind_contextvars(correlation_id=value)
    return value


def get_correlation_id() -> str | None:
    return _CORRELATION_ID.get()


def clear_correlation_id(token: Token[str | None] | None = None) -> None:
    if token is not None:
        _CORRELATION_ID.reset(token)
    else:
        _CORRELATION_ID.set(None)
    structlog.contextvars.clear_contextvars()


@contextmanager
def correlation_scope(correlation_id: str | None = None) -> Iterator[str]:
    token = _CORRELATION_ID.set(correlation_id or uuid.uuid4().hex)
    cid = _CORRELATION_ID.get()
    assert cid is not None
    structlog.contextvars.bind_contextvars(correlation_id=cid)
    try:
        yield cid
    finally:
        _CORRELATION_ID.reset(token)
        structlog.contextvars.clear_contextvars()


def configure_logging(*, level: int = logging.INFO, json_logs: bool = False) -> None:
    shared_processors: list[structlog.types.Processor] = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
    ]
    renderer: structlog.types.Processor = (
        structlog.processors.JSONRenderer() if json_logs else structlog.dev.ConsoleRenderer()
    )
    structlog.configure(
        processors=[
            *shared_processors,
            structlog.processors.format_exc_info,
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
    formatter = structlog.stdlib.ProcessorFormatter(
        processors=[structlog.stdlib.ProcessorFormatter.remove_processors_meta, renderer],
    )
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    root = logging.getLogger()
    root.handlers.clear()
    root.addHandler(handler)
    root.setLevel(level)


def get_logger(name: str, **initial_context: Any) -> structlog.stdlib.BoundLogger:
    return cast(structlog.stdlib.BoundLogger, structlog.get_logger(name).bind(**initial_context))

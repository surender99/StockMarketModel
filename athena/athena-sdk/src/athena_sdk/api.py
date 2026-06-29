"""Public API facade — ATH-REL-020."""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any


API_VERSION = "v1"


@dataclass
class RateLimitState:
    max_requests: int = 100
    window_seconds: int = 60
    _requests: list[float] = field(default_factory=list)

    def allow(self) -> bool:
        now = time.time()
        self._requests = [t for t in self._requests if now - t < self.window_seconds]
        if len(self._requests) >= self.max_requests:
            return False
        self._requests.append(now)
        return True


@dataclass
class OpenAPISpec:
    title: str = "Athena API"
    version: str = API_VERSION
    paths: dict[str, dict[str, Any]] = field(default_factory=dict)

    def add_path(self, path: str, methods: dict[str, Any]) -> None:
        self.paths[path] = methods

    def to_dict(self) -> dict[str, Any]:
        return {"openapi": "3.0.0", "info": {"title": self.title, "version": self.version}, "paths": self.paths}


class RestAPIFacade:
    """REST API stub — REQ-SDK-REST-001."""

    def __init__(self, rate_limit: RateLimitState | None = None) -> None:
        self.rate_limit = rate_limit or RateLimitState()
        self.spec = OpenAPISpec()
        self._handlers: dict[str, Any] = {}

    def register(self, path: str, handler) -> None:
        self._handlers[path] = handler
        self.spec.add_path(path, {"get": {"summary": path}})

    def call(self, path: str, **kwargs: Any) -> dict[str, Any]:
        if not self.rate_limit.allow():
            return {"error": "rate_limit_exceeded", "version": API_VERSION}
        handler = self._handlers.get(path)
        if handler is None:
            return {"error": "not_found", "version": API_VERSION}
        return {"version": API_VERSION, "data": handler(**kwargs)}


class WebSocketFacade:
    """WebSocket API stub — REQ-SDK-WS-001."""

    def __init__(self) -> None:
        self._channels: dict[str, list[dict[str, Any]]] = {}

    def subscribe(self, channel: str) -> None:
        self._channels.setdefault(channel, [])

    def publish(self, channel: str, message: dict[str, Any]) -> None:
        self._channels.setdefault(channel, []).append(message)

    def drain(self, channel: str) -> list[dict[str, Any]]:
        msgs = self._channels.get(channel, [])
        self._channels[channel] = []
        return msgs

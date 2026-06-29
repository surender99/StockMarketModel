"""Dependency injection container — ATH-REL-001 §02-Dependency-Injection."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any, TypeVar

from athena_core.domain.errors import ConfigurationError, NotFoundError

T = TypeVar("T")
Factory = Callable[[], T]


class ServiceContainer:
    """Lightweight service registry with singleton and transient lifecycles."""

    def __init__(self) -> None:
        self._factories: dict[str, Factory[Any]] = {}
        self._singletons: dict[str, bool] = {}
        self._instances: dict[str, Any] = {}

    def register(
        self,
        key: str,
        factory: Factory[T],
        *,
        singleton: bool = True,
    ) -> None:
        if key in self._factories:
            msg = f"service already registered: {key}"
            raise ConfigurationError(msg, context={"service": key})
        self._factories[key] = factory
        self._singletons[key] = singleton

    def resolve(self, key: str) -> Any:
        if key not in self._factories:
            msg = f"unknown service: {key}"
            raise NotFoundError(msg, context={"service": key})
        if self._singletons[key]:
            if key not in self._instances:
                self._instances[key] = self._factories[key]()
            return self._instances[key]
        return self._factories[key]()

    def has(self, key: str) -> bool:
        return key in self._factories

    def clear(self) -> None:
        self._factories.clear()
        self._singletons.clear()
        self._instances.clear()

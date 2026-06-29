"""Core framework tests — ATH-REL-001."""

from __future__ import annotations

from datetime import date, datetime, timezone

import pytest

from athena_core.application.bootstrap import bootstrap_athena_core
from athena_core.application.config import AthenaConfig
from athena_core.application.container import ServiceContainer
from athena_core.domain.common import Identifier, SemanticVersion, ensure_date, to_json_safe, utc_now
from athena_core.domain.errors import AthenaError, ConfigurationError, ErrorCode, NotFoundError
from athena_core.domain.events import DomainEvent, EventBus
from athena_core.domain.plugins import Plugin, PluginLifecycle, PluginMetadata, PluginRegistry, PluginType
from athena_core.infrastructure.logging import (
    bind_correlation_id,
    clear_correlation_id,
    correlation_scope,
    get_correlation_id,
)


def test_service_container_singleton_and_transient() -> None:
    container = ServiceContainer()
    container.register("counter", lambda: {"n": 0}, singleton=True)
    container.register("fresh", lambda: object(), singleton=False)
    first = container.resolve("counter")
    second = container.resolve("counter")
    assert first is second
    assert container.resolve("fresh") is not container.resolve("fresh")


def test_service_container_unknown_raises() -> None:
    container = ServiceContainer()
    with pytest.raises(NotFoundError, match="unknown service"):
        container.resolve("missing")


def test_service_container_duplicate_raises() -> None:
    container = ServiceContainer()
    container.register("svc", lambda: 1)
    with pytest.raises(ConfigurationError, match="already registered"):
        container.register("svc", lambda: 2)


def test_event_bus_publish_and_subscribe() -> None:
    bus = EventBus()
    seen: list[str] = []
    bus.subscribe("ingest.completed", lambda event: seen.append(event.event_type))
    bus.publish(DomainEvent(event_type="ingest.completed", payload={"symbol": "RELIANCE.NS"}))
    assert seen == ["ingest.completed"]


def test_event_bus_handler_failure_wraps_athena_error() -> None:
    bus = EventBus()

    def boom(_event: DomainEvent) -> None:
        raise RuntimeError("boom")

    bus.subscribe("fail", boom)
    with pytest.raises(AthenaError, match="event handler failed"):
        bus.publish(DomainEvent(event_type="fail"))


def test_domain_error_codes() -> None:
    err = NotFoundError("missing", context={"id": "x"})
    assert err.code == ErrorCode.NOT_FOUND
    assert "ATH-NF-001" in str(err)


def test_core_utilities() -> None:
    assert str(Identifier("ema")) == "ema"
    assert str(SemanticVersion("1.0.0")) == "1.0.0"
    with pytest.raises(ValueError):
        SemanticVersion("bad")
    assert ensure_date("2024-01-15") == date(2024, 1, 15)
    payload = to_json_safe({"when": datetime(2024, 1, 15, tzinfo=timezone.utc)})
    assert payload["when"].startswith("2024-01-15")
    assert utc_now().tzinfo is not None


def test_correlation_id_binding() -> None:
    cid = bind_correlation_id("trace-123")
    assert get_correlation_id() == "trace-123"
    clear_correlation_id()
    assert get_correlation_id() is None

    with correlation_scope("scope-1") as active:
        assert active == "scope-1"
        assert get_correlation_id() == "scope-1"
    assert get_correlation_id() is None


def test_plugin_lifecycle_and_discovery() -> None:
    registry = PluginRegistry()
    plugin = Plugin(
        id="rsi",
        version="1.0.0",
        plugin_type=PluginType.INDICATOR,
        metadata=PluginMetadata(name="RSI"),
    )
    registry.register(plugin, activate=False)
    assert plugin.lifecycle == PluginLifecycle.REGISTERED
    registry.activate("rsi")
    assert plugin.lifecycle == PluginLifecycle.ACTIVE
    registry.disable("rsi")
    assert plugin.lifecycle == PluginLifecycle.DISABLED
    assert registry.list(active_only=True) == []
    added = registry.discover(
        [
            Plugin(
                id="rsi",
                version="1.0.0",
                plugin_type=PluginType.INDICATOR,
                metadata=PluginMetadata(name="RSI"),
            ),
            Plugin(
                id="macd",
                version="1.0.0",
                plugin_type=PluginType.INDICATOR,
                metadata=PluginMetadata(name="MACD"),
            ),
        ]
    )
    assert added == 1
    registry.unregister("macd")
    assert registry.list() == [plugin]


def test_bootstrap_wires_core_context() -> None:
    ctx = bootstrap_athena_core(AthenaConfig())
    assert ctx.container.has("config")
    assert ctx.container.resolve("config") is ctx.config
    assert isinstance(ctx.plugin_registry, PluginRegistry)
    assert isinstance(ctx.event_bus, EventBus)

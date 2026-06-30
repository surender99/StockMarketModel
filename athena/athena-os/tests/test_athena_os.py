"""athena-os unit tests."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest
import yaml
from pydantic import BaseModel

from athena_os.configuration import ConfigurationManager
from athena_os.errors import EventError, NotFoundError
from athena_os.event_bus import DomainEvent, EventBus
from athena_os.messaging import Message, MessageBroker
from athena_os.metrics import MetricsCollector
from athena_os.plugins import Plugin, PluginLifecycle, PluginMetadata, PluginRegistry, PluginType
from athena_os.registry import Registry
from athena_os.runtime import AthenaRuntime
from athena_os.scheduler import Scheduler
from athena_os.workflow import WorkflowEngine, WorkflowStatus, WorkflowStep


def test_event_bus_publish_subscribe() -> None:
    bus = EventBus()
    seen: list[str] = []
    bus.subscribe("test.event", lambda e: seen.append(e.event_type))
    bus.publish(DomainEvent(event_type="test.event", payload={"k": "v"}))
    assert seen == ["test.event"]


def test_event_bus_handler_failure() -> None:
    bus = EventBus()

    def boom(_event: DomainEvent) -> None:
        raise RuntimeError("boom")

    bus.subscribe("fail", boom)
    with pytest.raises(EventError, match="event handler failed"):
        bus.publish(DomainEvent(event_type="fail"))


def test_registry_register_get() -> None:
    reg: Registry[str] = Registry("test")
    reg.register("a", "alpha")
    assert reg.get("a") == "alpha"
    assert reg.list_keys() == ["a"]


def test_registry_not_found() -> None:
    reg: Registry[str] = Registry()
    with pytest.raises(NotFoundError):
        reg.get("missing")


def test_configuration_load_yaml(tmp_path: Path) -> None:
    config_file = tmp_path / "app.yaml"
    config_file.write_text(yaml.dump({"app": {"name": "athena"}}), encoding="utf-8")
    mgr = ConfigurationManager(base_path=tmp_path)
    data = mgr.load_file("app.yaml")
    assert data["app"]["name"] == "athena"


def test_configuration_load_model(tmp_path: Path) -> None:
    class AppConfig(BaseModel):
        name: str

    config_file = tmp_path / "app.json"
    config_file.write_text('{"name": "athena"}', encoding="utf-8")
    mgr = ConfigurationManager(base_path=tmp_path)
    model = mgr.load_model("app.json", AppConfig)
    assert model.name == "athena"


def test_plugin_registry_lifecycle() -> None:
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


def test_runtime_bootstrap() -> None:
    runtime = AthenaRuntime.bootstrap()
    assert runtime.event_bus.handler_count() == 0
    assert isinstance(runtime.metrics, MetricsCollector)


def test_workflow_engine() -> None:
    engine = WorkflowEngine()
    engine.define(
        "ingest",
        [
            WorkflowStep("load", lambda ctx: {**ctx, "rows": 10}),
            WorkflowStep("validate", lambda ctx: {**ctx, "valid": True}),
        ],
    )
    result = engine.run("ingest")
    assert result.status == WorkflowStatus.COMPLETED
    assert result.context["rows"] == 10


def test_scheduler_run_due() -> None:
    sched = Scheduler()
    seen: list[str] = []

    def job() -> str:
        seen.append("ok")
        return "ok"

    sched.schedule("job", datetime.now(tz=timezone.utc) - timedelta(seconds=1), job)
    assert sched.run_due() == ["ok"]
    assert seen == ["ok"]


def test_messaging_broker() -> None:
    broker = MessageBroker()
    received: list[dict] = []
    broker.subscribe("alerts", received.append)
    broker.publish(Message(topic="alerts", payload={"level": "info"}))
    assert received == [{"level": "info"}]


def test_metrics_collector() -> None:
    metrics = MetricsCollector()
    metrics.increment("requests", service="core")
    metrics.gauge("latency_ms", 12.5)
    metrics.observe("duration", 0.5)
    snap = metrics.snapshot()
    assert snap["counters"]["requests{service=core}"] == 1.0
    assert snap["gauges"]["latency_ms"] == 12.5

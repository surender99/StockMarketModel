# Interface Catalog — Master Index

> **Updated:** 2026-06-30

| # | Name | Package | Version | Consumers |
|---|------|---------|---------|-----------|
| 1 | `EventBus` | `athena-os` | 1.0.0 | athena-core, bootstrap |
| 2 | `DomainEvent` | `athena-os` | 1.0.0 | athena-core, SDK |
| 3 | `PluginRegistry` | `athena-os` | 1.0.0 | athena-core, feature pipeline |
| 4 | `ConfigurationManager` | `athena-os` | 1.0.0 | athena-core, CLI |
| 5 | `AthenaRuntime` | `athena-os` | 1.0.0 | athena-core bootstrap |
| 6 | `Registry` | `athena-os` | 1.0.0 | service discovery |
| 7 | `WorkflowEngine` | `athena-os` | 1.0.0 | research pipelines |
| 8 | `Scheduler` | `athena-os` | 1.0.0 | simulation, jobs |
| 9 | `MetricsCollector` | `athena-os` | 1.0.0 | observability |
| 10 | `MessageBroker` | `athena-os` | 1.0.0 | async stubs |
| 11 | `RBACAuthorizer` | `athena-os` | 1.0.0 | security_manager |
| 12 | `SecretsVault` | `athena-os` | 1.0.0 | production, CLI |
| 13 | `ServiceContainer` | `athena-core` | 1.0.0 | bootstrap, SDK |
| 14 | `AthenaConfig` | `athena-core` | 1.0.0 | CLI, dashboard, AI |
| 15 | `bootstrap_athena_core` | `athena-core` | 1.0.0 | SDK, CLI, tests |
| 16 | `IndicatorEngine` | `athena-core` | 1.0.0 | strategy, research |
| 17 | `PatternPipeline` | `athena-core` | 1.0.0 | strategy, dashboard |
| 18 | `BacktestEngine` | `athena-core` | 1.0.0 | research, CLI |
| 19 | `ResearchEventBus` | `athena-core` | 1.0.0 | QREP modules |
| 20 | `SimulationEventBus` | `athena-core` | 1.0.0 | simulation stack |
| 21 | `AthenaClient` | `athena-sdk` | 1.0.0 | CLI, dashboard, external |
| 22 | `RestAPIFacade` | `athena-sdk` | 1.0.0 | HTTP adapters |
| 23 | `WebSocketFacade` | `athena-sdk` | 1.0.0 | realtime dashboard |

---

## Signatures

### `EventBus` — `athena_os.event_bus`

```python
class EventBus:
    def subscribe(self, event_type: str, handler: EventHandler) -> None: ...
    def unsubscribe(self, event_type: str, handler: EventHandler) -> None: ...
    def publish(self, event: DomainEvent) -> list[Any]: ...
    def clear(self, event_type: str | None = None) -> None: ...
```

**Consumers:** `athena_core.application.bootstrap`, tests

### `PluginRegistry` — `athena_os.plugins`

```python
class PluginRegistry:
    def register(self, plugin: Plugin, *, activate: bool = True) -> None: ...
    def get(self, plugin_id: str) -> Plugin: ...
    def list(self, plugin_type: PluginType | None = None, *, active_only: bool = False) -> list[Plugin]: ...
    def discover(self, plugins: Iterable[Plugin], *, activate: bool = True) -> int: ...
```

**Consumers:** `athena_core.application.bootstrap`, indicator/pattern plugins

### `ConfigurationManager` — `athena_os.configuration`

```python
class ConfigurationManager:
    def load_file(self, path: Path | str) -> dict[str, Any]: ...
    def load_model(self, path: Path | str, model: type[BaseModel]) -> BaseModel: ...
```

**Consumers:** CLI config loading, runtime bootstrap

### `ServiceContainer` — `athena_core.application.container`

```python
class ServiceContainer:
    def register(self, key: str, factory: Factory[T], *, singleton: bool = True) -> None: ...
    def resolve(self, key: str) -> Any: ...
    def has(self, key: str) -> bool: ...
```

**Consumers:** `bootstrap_athena_core`, `AthenaClient`

### `bootstrap_athena_core` — `athena_core.application.bootstrap`

```python
def bootstrap_athena_core(config: AthenaConfig, *, wire_data: bool = True) -> CoreContext: ...
```

**Consumers:** `athena-sdk`, `athena-cli`, integration tests

### `AthenaClient` — `athena_sdk.client`

```python
class AthenaClient:
    def __init__(self, config: AthenaConfig | None = None) -> None: ...
    # Facade over core services
```

**Consumers:** CLI, dashboard, external integrations

### `SimulationEventBus` — `athena_core.domain.simulation.event_bus`

```python
class SimulationEventBus:
    def subscribe(self, event_type: SimulationEventType, handler: Handler) -> None: ...
    def publish(self, event: SimulationEvent) -> None: ...
    def replay(self, events: list[SimulationEvent]) -> None: ...
```

**Consumers:** market simulator, OMS, portfolio

### `ResearchEventBus` — `athena_core.domain.research.events`

```python
class ResearchEventBus:
    def publish(self, event: ResearchEvent) -> None: ...
    def drain(self) -> list[ResearchEvent]: ...
    def replay(self, events: list[ResearchEvent]) -> None: ...
```

**Consumers:** experiment engine, reproducibility, reporting

---

## References

- [ADR-0005 AthenaOS](../adrs/ADR-0005-athena-os.md)
- [ATH-REL-020 SDK](../ATH-REL-020-SDK-and-Public-APIs.md)

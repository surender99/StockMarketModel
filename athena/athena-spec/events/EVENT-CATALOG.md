# Event Catalog — Master Index

> **Updated:** 2026-06-30  
> **YAML sources:** [registry/](registry/) — run `make codegen` to regenerate Python event classes  
> **Infrastructure bus:** `athena_os.event_bus.EventBus`  
> **Domain buses:** simulation, research (see below)

| # | Event Name | Publisher | Subscribers | Version | Compatibility |
|---|------------|-----------|-------------|---------|---------------|
| 1 | `ingest.completed` | `athena_core.application.data_bootstrap` | pipelines, feature store | 1.0.0 | additive |
| 2 | `ingest.failed` | `athena_core.application.data_bootstrap` | observability, retry jobs | 1.0.0 | additive |
| 3 | `data.validated` | `athena_core.domain.data.quality` | ingest, registry | 1.0.0 | additive |
| 4 | `feature.computed` | `athena_core.application.feature_pipeline` | strategy, research | 1.0.0 | additive |
| 5 | `indicator.registered` | `athena_core.domain.features.indicator_plugins` | plugin registry | 1.0.0 | additive |
| 6 | `pattern.detected` | `athena_core.domain.patterns.pipeline` | strategy, dashboard | 1.0.0 | additive |
| 7 | `signal.generated` | `athena_core.domain.strategy.signals` | backtest, paper trading | 1.0.0 | additive |
| 8 | `strategy.evaluated` | `athena_core.domain.strategy.engine` | portfolio, reporting | 1.0.0 | additive |
| 9 | `simulation.market` | `athena_core.domain.simulation.market_simulator` | OMS, portfolio | 1.0.0 | additive |
| 10 | `simulation.order` | `athena_core.domain.simulation.oms` | execution, journal | 1.0.0 | additive |
| 11 | `simulation.portfolio` | `athena_core.domain.simulation.portfolio` | risk, reporting | 1.0.0 | additive |
| 12 | `simulation.corporate_action` | `athena_core.domain.simulation.corporate_actions` | positions, pricing | 1.0.0 | additive |
| 13 | `simulation.timer` | `athena_core.domain.simulation.scheduler` | session, replay | 1.0.0 | additive |
| 14 | `research.project_created` | `athena_core.domain.research.projects` | experiment engine | 1.0.0 | additive |
| 15 | `research.experiment_started` | `athena_core.domain.research.experiments` | reproducibility, events | 1.0.0 | additive |
| 16 | `research.experiment_completed` | `athena_core.domain.research.experiments` | reporting, catalog | 1.0.0 | additive |
| 17 | `research.dataset_snapshot_created` | `athena_core.domain.research.datasets` | lineage, validation | 1.0.0 | additive |
| 18 | `research.hypothesis_validated` | `athena_core.domain.research.hypothesis` | knowledge base | 1.0.0 | additive |
| 19 | `portfolio.rebalanced` | `athena_core.domain.portfolio_intelligence.rebalancer` | risk, audit | 1.0.0 | additive |
| 20 | `security.audit` | `athena_os.security.SecurityAuditTrail` | compliance, logging | 1.0.0 | additive |

---

## Payload Summaries

### `ingest.completed` (v1.0.0)

```json
{
  "symbol": "RELIANCE.NS",
  "rows": 252,
  "source": "yfinance",
  "bar_frequency": "1d"
}
```

**Publisher:** `athena_core.application.data_bootstrap`  
**Subscribers:** feature pipeline, dataset registry  
**Compatibility:** additive

### `simulation.order` (v1.0.0)

```json
{
  "order_id": "ord-001",
  "symbol": "AAPL",
  "side": "buy",
  "quantity": 100,
  "status": "filled"
}
```

**Publisher:** `athena_core.domain.simulation.oms.SimulationEventBus`  
**Subscribers:** trade journal, portfolio updater  
**Compatibility:** additive

### `research.experiment_started` (v1.0.0)

```json
{
  "project_id": "proj-001",
  "experiment_id": "exp-001",
  "hypothesis_id": "hyp-001"
}
```

**Publisher:** `athena_core.domain.research.events.ResearchEventBus`  
**Subscribers:** reproducibility engine, benchmark suite  
**Compatibility:** additive

### `signal.generated` (v1.0.0)

```json
{
  "strategy_id": "ema_cross",
  "symbol": "INFY.NS",
  "direction": "long",
  "strength": 0.82
}
```

**Publisher:** `athena_core.domain.strategy.signals`  
**Subscribers:** backtest engine, paper trading  
**Compatibility:** additive

### `security.audit` (v1.0.0)

```json
{
  "event_type": "login",
  "user_id": "u-001",
  "resource": "/api/research",
  "details": {}
}
```

**Publisher:** `athena_os.security.SecurityAuditTrail`  
**Subscribers:** compliance checker, structured logs  
**Compatibility:** additive

---

## Domain Event Type Enums

| Bus | Enum | Location |
|-----|------|----------|
| Simulation | `SimulationEventType` | `athena_core.domain.simulation.event_bus` |
| Research | `ResearchEventType` | `athena_core.domain.research.events` |
| Infrastructure | string event types | `athena_os.event_bus.DomainEvent` |

## References

- [APS-004 Event Bus](../ATHENA/APS/Foundation/APS-004-Event-Bus.md)
- [ADR-0005 AthenaOS](../adrs/ADR-0005-athena-os.md)

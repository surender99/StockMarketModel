# AES-0201 – Clean Architecture

> **Canonical repo layout:** [ATH-003-Repository-Architecture.md](../ATH-003-Repository-Architecture.md)  
> **References source:** `References/Athena-Package-02-Architecture/architecture/AES-0201-Clean-Architecture.md`

Dependency rules and layer mapping for `athena-core` and sibling packages.

---

## Dependency Rule

Dependencies point **inward**. Outer layers orchestrate; inner layers define behavior.

```
interfaces/          ← CLI, future REST/API adapters
    ↓
application/         ← Use cases, orchestration, engines
    ↓
domain/              ← Entities, value objects, ports — no I/O
    ↑
infrastructure/      ← Implements domain ports (Parquet, yfinance, YAML)
```

**Domain contains no framework-specific code** — no `structlog`, no `yfinance`, no file paths in domain modules. Infrastructure and application may use third-party libraries.

---

## Layer Mapping (`athena-core`)

| Layer | Path | Responsibility | Examples |
|-------|------|----------------|----------|
| **Domain** | `domain/` | Pure business logic, entities, ports | `OHLCVBar`, `StrategyConfig`, `compute_ema`, `OHLCVRepositoryPort` |
| **Application** | `application/` | Use cases and orchestration | `BacktestEngine`, `FeatureService`, `Scanner`, `Optimizer` |
| **Infrastructure** | `infrastructure/` | External I/O adapters | `ParquetOHLCVStore`, `YFinanceClient`, `StrategyYamlLoader` |
| **Interfaces** | `interfaces/` | Delivery mechanisms | `cli.py` |

### Dependency matrix

| From → To | domain | application | infrastructure | interfaces |
|-----------|--------|-------------|----------------|------------|
| domain | ✅ | ❌ | ❌ | ❌ |
| application | ✅ | ✅ | ❌ | ❌ |
| infrastructure | ✅ | ❌ | ✅ | ❌ |
| interfaces | ✅ | ✅ | ✅* | ✅ |

\* Interfaces may construct infrastructure adapters at the composition root (`runtime.py`) — dependency injection at the edge only.

---

## Ports and Adapters

Domain **ports** define what the application needs without specifying how:

| Port | Location | Infrastructure adapter |
|------|----------|------------------------|
| `OHLCVRepositoryPort` | `domain/ports/ohlcv_repository.py` | `ParquetOHLCVStore` |
| `FeatureStorePort` | `domain/ports/feature_store.py` | `ParquetFeatureStore` |
| `TradingCalendarPort` | `domain/ports/trading_calendar.py` | `NSECalendar` |
| `FeatureProviderPort` | `application/backtest_engine.py` | `FeatureServiceProvider` |

Application code depends on port **protocols**, not concrete stores.

---

## Sibling Packages

| Package | Clean Architecture role |
|---------|-------------------------|
| `athena-ai` | `domain/` (intent, research plan), `application/` (orchestrator), `infrastructure/` (OpenAI) |
| `athena-sdk` | Thin facade over `athena-core` application services |
| `athena-cli` | Interface layer — parses args, calls `athena-core` runtime |
| `athena-dashboard` | Interface layer — Streamlit over SDK/core |

Each package follows the same inward dependency rule within its own `src/` tree.

---

## Enforcement

- **Lint / import checks:** Domain modules must not import from `infrastructure/` or `interfaces/`.
- **Tests:** Unit tests for domain and application use fakes/mocks of ports — no disk or network in domain tests.
- **REQ traceability:** Every feature REQ names the layer it extends ([ATH-004](../ATH-004-Requirement-Standard.md)).

---

## Related Documents

| Document | Purpose |
|----------|---------|
| [ATH-003 Repository Architecture](../ATH-003-Repository-Architecture.md) | Monorepo layout |
| [ATH-002 Engineering Standards](../ATH-002-Engineering-Standards.md) | Coding and testing standards |
| [AES-0200 System Architecture](AES-0200-System-Architecture.md) | Full system layers |
| [AES-0202 Plugin Architecture](AES-0202-Plugin-Architecture.md) | Plugin registration model |

# ADR-0005 – AthenaOS Infrastructure Layer

> **Status:** Accepted  
> **Date:** 2026-06-30  
> **Deciders:** Athena platform architects

## Context

Foundation infrastructure (event bus, configuration, plugins, logging, security stubs) was embedded in `athena-core` under `domain/` and `infrastructure/`. As the platform grows across core, SDK, CLI, dashboard, and AI packages, infrastructure concerns must not be duplicated or provided by domain packages.

## Decision

Introduce **`athena-os`** (`athena/athena-os/`) as the **sole infrastructure layer** that all Athena Python packages depend on.

| Module | Responsibility |
|--------|----------------|
| `event_bus` | Domain event publish/subscribe |
| `workflow` | Workflow orchestration |
| `scheduler` | Task scheduling |
| `registry` | Generic named-object registry |
| `configuration` | YAML/JSON configuration loading |
| `plugins` | Plugin framework and lifecycle |
| `security` | RBAC, secrets vault, audit trail stubs |
| `logging` | Structured logging with correlation IDs |
| `metrics` | Metrics collection stubs |
| `messaging` | In-process message broker |
| `runtime` | Shared runtime composition root |

`athena-core` re-exports infrastructure types for backward compatibility but **imports from `athena_os`**, not duplicate implementations.

## Dependency Rule

```
athena-os  ←  athena-core  ←  { athena-ai, athena-dashboard, athena-sdk, athena-cli }
```

No package other than `athena-os` may provide cross-cutting infrastructure.

## Statistics Independence

Quantitative statistics and analytics remain in **`athena_core.domain.analytics`** and **`athena_core.domain.statistics`**, not in indicators or `athena-os`. Indicators compute technical values; analytics performs hypothesis tests, correlation, and distribution analysis. See [SPEC-VS-CODE-STATUS.md](../SPEC-VS-CODE-STATUS.md).

## Alternatives Considered

| Option | Pros | Cons |
|--------|------|------|
| **Dedicated athena-os package** (chosen) | Clear boundary; single source of truth | Migration effort from embedded core modules |
| **Keep infra in athena-core** | No new package | SDK/CLI would duplicate or depend on full core |
| **External framework (e.g. Celery)** | Battle-tested | Overkill for MVP; violates minimal-deps principle |

## Consequences

- **Positive:** Clean layering; infrastructure testable in isolation; APS-001–015 map to `athena-os`.
- **Negative:** Short-term shim modules in `athena-core` until imports are fully migrated.
- **Neutral:** Domain-specific event buses (simulation, research) remain in `athena-core` but are catalogued in `athena-spec/events/`.

## Compliance

- [x] [ATH-003 Repository Architecture](../ATH-003-Repository-Architecture.md)
- [x] [APS-004 Event Bus](../ATHENA/APS/Foundation/APS-004-Event-Bus.md)

## References

- [ADR-0004 Consolidated Monorepo](ADR-0004-consolidated-monorepo.md)
- [DEPENDENCY-RULES.md](../ATHENA/DEPENDENCY-RULES.md)

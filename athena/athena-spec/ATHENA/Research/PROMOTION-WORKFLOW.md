# Research → Production Promotion Workflow

> **Package:** `athena-research` (non-production)  
> **Production:** `athena-platform` + bounded contexts

## Stages

```
Research → Experiment → Promote → Production
```

| Stage | Package | Artifact |
|-------|---------|----------|
| **Research** | `athena-research` | Hypothesis, notebook, draft strategy |
| **Experiment** | `athena-core.domain.research` | Experiment run, dataset snapshot, metrics |
| **Promote** | Governance review | ADR, APS traceability, golden tests |
| **Production** | `athena-platform` | Registered plugin, feature flag on, event contracts |

## Promotion Gates

1. All pytest and architecture tests pass (`make test`).
2. Event YAML registered in `athena-spec/events/registry/`.
3. `module.yaml` updated with publishes/consumes events.
4. Dependency rules satisfied (`make deps-check`).
5. Performance benchmarks meet [PERFORMANCE-GATES.md](../Benchmarks/PERFORMANCE-GATES.md).

## Rollback

Disable feature flag in `PlatformFeatures` without removing plugin registration.

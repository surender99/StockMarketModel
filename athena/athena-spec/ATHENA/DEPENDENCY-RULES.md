# Dependency Rules

> **Enforced by:** `athena/scripts/check_dependencies.py`  
> **Architecture fitness tests:** `athena-testing/architecture/` (CI build breakers)  
> **ADR:** [ADR-0005-athena-os](../adrs/ADR-0005-athena-os.md), [ADR-0006](../adrs/ADR-0006-bounded-contexts.md), [ADR-0007](../adrs/ADR-0007-rich-module-manifests.md)

## Layer Model

```
athena-common                ← pure domain types (no infra)
    ↑
athena-os                    ← infrastructure only (no domain deps)
    ↑
athena-domain                ← Protocol contracts
athena-core                  ← domain + application (depends on athena-os, athena-common)
    ↑
{ athena-core-runtime, athena-core-events, athena-core-engine, athena-core-metadata }  ← core facades
{ athena-data, athena-indicators, athena-patterns, athena-strategies,
  athena-risk, athena-portfolio, athena-execution }   ← bounded contexts
{ athena-metadata, athena-observability, athena-market, athena-brokers }  ← extension facades
    ↑
athena-platform              ← production assembly
    ↑
{ athena-ai, athena-dashboard, athena-sdk, athena-cli }   ← interface adapters
```

## Rules

| Rule | Description |
|------|-------------|
| **R1** | `athena-os` must not depend on `athena-core` or any interface package |
| **R2** | `athena-core` must depend on `athena-os` for infrastructure |
| **R3** | Interface packages may depend on `athena-core` and `athena-os` but not on each other |
| **R4** | No circular dependencies between any packages |
| **R5** | Domain statistics/analytics stay in `athena_core.domain.analytics` — not in indicators or `athena-os` |
| **R6** | `athena-indicators` must not import `athena-portfolio`, `athena-execution`, or `athena-strategies` |
| **R7** | `athena-research` must not import production execution paths (`athena-execution`, `athena-platform`) |
| **R8** | Rich `module.yaml` manifests must declare `owner`, `bounded_context`, and `version` (ADR-0007) |

## Forbidden Import Matrix (fitness tests)

| Package | Must NOT import |
|---------|-----------------|
| `athena-indicators` | `athena_portfolio`, `athena_execution`, `athena_strategies` |
| `athena-patterns` | `athena_portfolio`, `athena_execution` |
| `athena-data` | `athena_strategies`, `athena_portfolio` |
| `athena-research` | `athena_execution`, `athena_platform`, production managers |

## CI Build Breakers

Architecture fitness tests run as part of `make test` via `athena-testing`:

| Test module | Enforces |
|-------------|----------|
| `test_forbidden_dependencies.py` | Cross-context import bans (R6–R7) |
| `test_no_cycles.py` | Acyclic package graph (R4) |
| `test_bounded_context_rules.py` | Manifest `bounded_context` and allowlists |
| `test_api_compatibility.py` | Public `__all__` / Protocol stability |
| `test_event_compatibility.py` | Event YAML versions match generated code |

```bash
cd athena && make test
python athena/scripts/check_dependencies.py
```

Exit code 0 = all rules satisfied.

## References

- [MANIFEST-SCHEMA.yaml](../metadata/MANIFEST-SCHEMA.yaml)
- [CODEGEN-STANDARD.md](../codegen/CODEGEN-STANDARD.md)

# Dependency Rules

> **Enforced by:** `athena/scripts/check_dependencies.py`  
> **ADR:** [ADR-0005-athena-os](../adrs/ADR-0005-athena-os.md)

## Layer Model

```
athena-common                ← pure domain types (no infra)
athena-os                    ← infrastructure only (no domain deps)
    ↑
athena-domain                ← Protocol contracts
athena-core                  ← domain + application (depends on athena-os, athena-common)
    ↑
{ athena-data, athena-indicators, athena-patterns, athena-strategies,
  athena-risk, athena-portfolio, athena-execution }   ← facade bounded contexts
    ↑
athena-platform              ← production assembly
    ↑
{ athena-ai, athena-dashboard, athena-sdk, athena-cli }   ← interface adapters
```

See [ADR-0006](../adrs/ADR-0006-bounded-contexts.md) for facade extraction strategy.

## Rules

| Rule | Description |
|------|-------------|
| **R1** | `athena-os` must not depend on `athena-core` or any interface package |
| **R2** | `athena-core` must depend on `athena-os` for infrastructure |
| **R3** | Interface packages may depend on `athena-core` and `athena-os` but not on each other |
| **R4** | No circular dependencies between any packages |
| **R5** | Domain statistics/analytics stay in `athena_core.domain.analytics` — not in indicators or `athena-os` |

## Allowed Dependency Matrix

| Package | athena-os | athena-core | athena-sdk | athena-cli | athena-ai | athena-dashboard |
|---------|-----------|-------------|------------|------------|-----------|------------------|
| athena-os | — | ✗ | ✗ | ✗ | ✗ | ✗ |
| athena-core | ✓ | — | ✗ | ✗ | ✗ | ✗ |
| athena-sdk | ✓ | ✓ | — | ✗ | ✗ | ✗ |
| athena-cli | ✓ | ✓ | ✓ | — | ✓* | ✗ |
| athena-ai | ✓ | ✓ | ✓ | ✗ | — | ✗ |
| athena-dashboard | ✓ | ✓ | ✓ | ✗ | ✗ | — |
| athena-testing | ✓ | ✓ | ✗ | ✗ | ✗ | ✗ |

\* `athena-cli` may depend on `athena-ai` for research-assistant commands only.

## CI Check

```bash
python athena/scripts/check_dependencies.py
```

Exit code 0 = all rules satisfied.

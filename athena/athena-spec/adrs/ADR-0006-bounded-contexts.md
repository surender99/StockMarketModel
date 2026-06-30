# ADR-0006: Bounded Context Packages (Facade-First Extraction)

**Status:** Accepted  
**Date:** 2026-06-30

## Context

`athena-core` grew into a monolithic domain+application package. Architecture evolution requires bounded contexts (indicators, patterns, strategies, risk, portfolio, execution) with clear dependency rules and interface contracts.

## Decision

1. Create thin facade packages (`athena-indicators`, `athena-patterns`, etc.) that **re-export** existing `athena-core` code.
2. Define engine contracts in `athena-domain` using Python `Protocol`.
3. Implement adapters in each bounded-context package that delegate to `athena-core`.
4. Introduce `athena-common` for pure domain types and `athena-platform` for production assembly.
5. Keep all 409+ existing tests passing — **no big-bang move**.

## Extraction Path

```
Phase 1 (now):  facade packages → depend on athena-core
Phase 2:        move modules from core → bounded context packages
Phase 3:        athena-core becomes orchestration-only or shrinks
Phase 4:        consumers import bounded contexts directly
```

## Dependency Rules

- `athena-common` — no athena package deps
- `athena-domain` — `athena-common`, `athena-os` (protocols only)
- Bounded contexts — `athena-os`, `athena-common`, `athena-core` (temporary)
- `athena-platform` — wires os + core + bounded contexts
- `athena-core` — must not depend on bounded contexts (avoids cycles)

## Consequences

- Temporary duplication of package boundaries (facade vs implementation location).
- `check_dependencies.py` and architecture tests enforce layering.
- Event contracts move to YAML registry with codegen to `athena-common`.

## References

- [DEPENDENCY-RULES.md](../ATHENA/DEPENDENCY-RULES.md)
- [CAPABILITY-MAP.md](../ATHENA/CAPABILITY-MAP.md)
- ATH-002 Dependency Graph

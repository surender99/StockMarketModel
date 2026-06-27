# ADR-0003 – In-Process Plugin Registry (AES-0202)

> **Status:** Accepted  
> **Date:** 2026-06-27  
> **Deciders:** Athena platform architects

## Context

[AES-0202 Plugin Architecture](../architecture/AES-0202-Plugin-Architecture.md) defines pluggable indicators, patterns, strategies, and ML models. The MVP must support registration and lookup without operating a separate plugin host, package manager, or dynamic loading from untrusted sources.

## Decision

Implement an **in-process `PluginRegistry`** inside `athena-core` (`athena_core.domain.plugins`). Plugins are Python classes registered at application startup (composition root / `FeatureService`), not loaded from external wheel files or subprocess plugins.

## Alternatives Considered

| Option | Pros | Cons |
|--------|------|------|
| **In-process registry** (chosen) | Simple; type-safe; easy testing; matches monorepo deploy model | All plugins ship in same release artifact; no third-party plugin marketplace |
| **Entry-point / setuptools plugins** | Standard Python discovery (`importlib.metadata`) | Version skew; harder to audit; overkill for MVP indicator set |
| **External plugin server / gRPC** | Isolation; hot reload | Operational complexity; latency; not needed for research MVP |
| **Hardcoded only (no registry)** | Minimal code | Violates plugin-first principle (ATH-000); blocks Package 05–07 evolution |

## Consequences

- **Positive:** Clear contract (`id`, `version`, `execute`); stub exists today; migration path from `FeatureService._INDICATOR_REGISTRY` is documented in AES-0202.
- **Negative:** Third-party plugins require contributing to the monorepo or a future packaging ADR.
- **Neutral:** External plugin loading can be revisited when a stable `IndicatorProvider` / `PatternProvider` ecosystem emerges.

## Compliance

- [x] [ATH-003 Repository Architecture](../ATH-003-Repository-Architecture.md) layers respected
- [ ] [AES-0005 Quant Standards](../governance/AES-0005-Quant-Standards.md) (if research-impacting)
- [ ] Related REQ or RFC linked below

## References

- [AES-0202 Plugin Architecture](../architecture/AES-0202-Plugin-Architecture.md)
- `athena_core.domain.plugins.PluginRegistry`

# ADR-0007: Rich Module Manifests

**Status:** Accepted  
**Date:** 2026-07-01

## Context

Package manifests (`module.yaml`) used a minimal flat schema (layer, dependencies list, public_apis). Architecture fitness tests, dependency graphs, and codegen need structured metadata: owner, bounded context, events, interfaces, API surface, database touchpoints, and quality gates.

## Decision

1. Adopt **rich manifests** defined in [MANIFEST-SCHEMA.yaml](../metadata/MANIFEST-SCHEMA.yaml).
2. Required fields: `name`, `owner`, `bounded_context`, `version`.
3. Structured sections: `dependencies.packages`, `events`, `interfaces`, `api`, `database`, `quality`.
4. `athena/scripts/athena_inspector.py` reads rich manifests and emits dependency graph snippets.
5. `codegen/generate_manifests.py` may generate manifests from component metadata — **never hand-edit generated manifests** when sourced from codegen.
6. Architecture tests in `athena-testing/architecture/` validate manifest consistency and import rules.

## Migration

| Old field | New location |
|-----------|--------------|
| `layer` | `bounded_context` |
| `dependencies` (list) | `dependencies.packages` |
| `publishes_events` | `events.publishes` |
| `consumes_events` | `events.consumes` |
| `public_apis` | `api.modules` |

## Consequences

- `make graph` and inspector tools consume richer metadata.
- New packages (metadata, observability, market, brokers) ship manifests on creation.
- CI fitness tests treat manifest drift as a build breaker.

## References

- [ADR-0006](ADR-0006-bounded-contexts.md)
- [DEPENDENCY-RULES.md](../ATHENA/DEPENDENCY-RULES.md)
- [MANIFEST-SCHEMA.yaml](../metadata/MANIFEST-SCHEMA.yaml)

# Marketplace V2 Vision (Future)

> **Status:** Specification only — not implemented

## Scope

Future plugin marketplace for:

- Indicators and strategies
- ML models and risk plugins
- Third-party extensions with versioning and compatibility gates

## Principles

1. Semver for plugin manifests
2. Sandboxed loading via `athena-os` plugin registry
3. Revenue and attribution metadata in rich manifests (`owner`, `quality`)

## References

- [ADR-0007](../adrs/ADR-0007-rich-module-manifests.md)
- [DEPENDENCY-RULES.md](../DEPENDENCY-RULES.md)

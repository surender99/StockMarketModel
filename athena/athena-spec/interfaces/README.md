# Interface Catalog

> **Purpose:** Document public APIs consumed across Athena packages.  
> **Schema:** name, package, signature, version, consumers.

## Interface Spec Schema

| Field | Required | Description |
|-------|----------|-------------|
| Name | Yes | Class or function name |
| Package | Yes | Installable package (`athena-os`, `athena-core`, `athena-sdk`) |
| Signature | Yes | Public method/function signature |
| Version | Yes | API semver |
| Consumers | Yes | Packages or modules that call this interface |

## File Layout

```
athena-spec/interfaces/
  README.md
  INTERFACE-CATALOG.md
  IF-*.md               ← optional detail specs
```

## Versioning

Public interfaces follow semver. Breaking changes require ADR and major version bump on the package.

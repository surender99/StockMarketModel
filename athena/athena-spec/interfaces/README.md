# Interface Catalog

> **Purpose:** Document public APIs consumed across Athena packages.  
> **Schema:** name, package, signature, version, consumers.  
> **Reference package:** [ATH-004 Master Interface Catalog](00-README.md) (integrated from `References/ATH-004-Master-Interface-Catalog.zip`)

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
  00-README.md           ← ATH-004 reference package index
  INTERFACE-CATALOG.md   ← implementation-aware master index (23 interfaces)
  catalog/               ← domain-level Master-Interface-Catalog.md
  dto/                   ← DTO-Guidelines.md
  01-Interface-Principles.md …  ← ATH-004 governance standards
  examples/              ← sample interface specs
  templates/             ← Interface-Template.md
  IF-*.md               ← optional detail specs
```

## Versioning

Public interfaces follow semver. Breaking changes require ADR and major version bump on the package.

# Event Catalog

> **Purpose:** Canonical registry of domain and infrastructure events across Athena packages.  
> **Schema:** Each event spec documents name, publisher, subscribers, payload, version, and compatibility.  
> **Reference package:** [ATH-003 Master Event Catalog](00-README.md) (integrated from `References/ATH-003-Master-Event-Catalog.zip`)

## Event Spec Schema

| Field | Required | Description |
|-------|----------|-------------|
| Event Name | Yes | Dot-separated or snake_case identifier |
| Publisher | Yes | Package/module that emits the event |
| Subscribers | Yes | Known consumers (or `any`) |
| Payload | Yes | JSON-schema-like field description |
| Version | Yes | Semver of payload contract |
| Compatibility | Yes | `backward` \| `breaking` \| `additive` |

## File Layout

```
athena-spec/events/
  README.md              ← this file
  00-README.md           ← ATH-003 reference package index
  EVENT-CATALOG.md       ← implementation-aware master index (20 events)
  catalog/               ← domain-level Master-Event-Catalog.md
  01-Event-Naming.md …   ← ATH-003 governance standards
  examples/              ← sample event payloads
  templates/             ← Event-Specification-Template.md
  EVT-*.md               ← individual event specs (optional detail files)
```

## Adding Events

1. Add row to [EVENT-CATALOG.md](EVENT-CATALOG.md).
2. If payload is non-trivial, add `EVT-<domain>-<name>.md`.
3. Emit via `athena_os.event_bus.EventBus` (infrastructure) or domain-specific buses documented in catalog.

## Versioning Rules

- **additive:** New optional payload fields; old subscribers unaffected.
- **backward:** Deprecated fields retained; migration path documented.
- **breaking:** Major version bump; subscribers must update.

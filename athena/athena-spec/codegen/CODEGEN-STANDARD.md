# Code Generation Standard

> **Location:** `athena/codegen/`  
> **Makefile target:** `make codegen`

## Principles

1. **Source of truth** — YAML specs under `athena-spec/` (events, interfaces, metadata).
2. **Generated output** — committed to version control; CI verifies regeneration is a no-op.
3. **Idempotent** — running codegen twice produces identical output.
4. **No hand-edits** — generated files include an AUTO-GENERATED banner.

## Generators

| Script | Status | Input | Output |
|--------|--------|-------|--------|
| `generate_events.py` | **Working** | `athena-spec/events/registry/*.event.yaml` | `athena-common/src/athena_common/events_generated.py` |
| `generate_dtos.py` | Stub | `athena-spec/interfaces/` | TBD |
| `generate_interfaces.py` | Stub | `athena-spec/interfaces/catalog/` | TBD |

## Usage

```bash
make codegen
# or
python athena/scripts/generate_events.py
```

## Event YAML Schema

See [events/registry/schema.yaml](../events/registry/schema.yaml).

## Link to EVENT-CATALOG

Human-readable index: [events/EVENT-CATALOG.md](../events/EVENT-CATALOG.md) — links to YAML sources in `events/registry/`.

# Event Registry Standard

> **Source of truth:** `athena-spec/events/registry/*.event.yaml`  
> **Generated code:** `athena-common/src/athena_common/events_generated.py`

## Required fields

| Field | Description |
|-------|-------------|
| `name` | PascalCase event name (e.g. `IndicatorCalculated`) |
| `publisher` | Bounded context that emits the event |
| `consumers` | List of subscribing contexts |
| `version` | Integer schema version |
| `compatibility` | `additive` or `breaking` |
| `description` | Human-readable summary |
| `payload` | Field name → primitive type map |
| `schema` | JSON Schema object (required for fitness tests) |

## Schema block

Each event must include a `schema` section mirroring `payload`:

```yaml
schema:
  type: object
  required: [symbol, indicator_id]
  properties:
    symbol: { type: string }
    indicator_id: { type: string }
```

Codegen embeds `SCHEMA` as a `ClassVar` on each generated event dataclass.

## Versioning

- Bump `version` on breaking payload changes.
- `test_event_compatibility.py` fails CI when YAML and generated code diverge.

## Regeneration

```bash
cd athena && make codegen
```

See [CODEGEN-STANDARD.md](../codegen/CODEGEN-STANDARD.md).

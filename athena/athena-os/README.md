# athena-os

Infrastructure layer for the Athena quantitative research platform. All Athena packages depend on `athena-os` for cross-cutting concerns; no other package provides infrastructure.

## Modules

| Module | Responsibility |
|--------|----------------|
| `event_bus` | In-process publish/subscribe domain events |
| `workflow` | Workflow engine (step orchestration) |
| `scheduler` | Task scheduling |
| `registry` | Generic named-object registry |
| `configuration` | YAML/JSON configuration loading |
| `plugins` | Plugin framework and lifecycle |
| `security` | RBAC, secrets vault, audit trail stubs |
| `logging` | Structured logging with correlation IDs |
| `metrics` | Metrics collection stubs |
| `messaging` | Message broker stubs |
| `runtime` | Shared runtime composition root |

## Install

```bash
pip install -e ".[dev]"
```

## Tests

```bash
pytest
```

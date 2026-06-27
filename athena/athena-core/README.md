# athena-core

Core library for Athena — data, indicators, strategies, and backtesting.

See [athena-spec](../athena-spec/README.md) for requirements and architecture.

## Install (development)

```bash
cd athena/athena-core
pip install -e ".[dev]"
```

## Run tests

```bash
pytest
```

## Layout

- `domain/` — entities and domain logic (no I/O)
- `application/` — use cases
- `infrastructure/` — adapters (logging, data sources)
- `interfaces/` — CLI and future API entry points

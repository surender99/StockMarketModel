# StockMarketModel — Athena

**Athena** is an AI-powered Quantitative Research Operating System for discovering, validating, and explaining robust trading strategies on Indian equities (NSE / NIFTY 500, daily OHLCV).

This repository hosts the Athena monorepo under [`athena/`](athena/).

## Quick Start

**Requirements:** Python 3.12+

```bash
cd athena/athena-core
pip install -e ".[dev]"
pytest
```

Optional (uv workspace):

```bash
uv sync
uv run --directory athena/athena-core pytest
```

Verify installation:

```bash
python -m athena_core.interfaces.cli health
```

## Documentation

Specifications live in [`athena/athena-spec/`](athena/athena-spec/README.md):

| Document | Purpose |
|----------|---------|
| [ATH-000 Philosophy](athena/athena-spec/ATH-000-Philosophy.md) | Mission and principles |
| [ATH-001 Vision & PRD](athena/athena-spec/ATH-001-Vision-PRD.md) | Product vision |
| [ATH-001 MVP Scope](athena/athena-spec/ATH-001-MVP-Scope.md) | Phase 1–2 scope |
| [ATH-002 Engineering Standards](athena/athena-spec/ATH-002-Engineering-Standards.md) | Code quality rules |
| [ATH-003 Repository Architecture](athena/athena-spec/ATH-003-Repository-Architecture.md) | Monorepo layout |
| [ATH-004 Requirement Standard](athena/athena-spec/ATH-004-Requirement-Standard.md) | REQ template |
| [Requirements backlog](athena/athena-spec/requirements/) | Traceable REQ specs |
| [Phase 0 Validation](athena/athena-spec/PHASE-0-VALIDATION.md) | Master validation report |

Legacy copy: [`Documents/`](Documents/README.md) (prefer `athena/athena-spec/`).

## Monorepo Layout

```
athena/
├── athena-spec/       # Specs, REQ backlog, validation
├── athena-core/       # Core library (Clean Architecture)
├── athena-ai/         # Future: AI research assistant
├── athena-docs/       # Future: documentation site
├── athena-sdk/        # Future: public SDK
├── athena-cli/        # Future: CLI package
└── athena-examples/   # Future: examples & notebooks
```

## Phase Roadmap

| Phase | Focus | Status |
|-------|-------|--------|
| **0** | Monorepo scaffold, specs, REQ backlog, engineering bootstrap | Complete |
| **1** | Data ingest, NSE calendar, EMA/SMA, feature store | Next |
| **2** | Strategy YAML, backtest engine, experiment tracking | Planned |
| **3** | Extended indicators, portfolio, optimization | Planned |
| **4+** | Regime, ML, scanner, dashboard | Planned |

See [PHASE-0-VALIDATION.md](athena/athena-spec/PHASE-0-VALIDATION.md) for Phase 1 handoff details.

## MVP Defaults

- **Market:** NSE, NIFTY 500, daily OHLCV
- **Data source:** yfinance (MVP)
- **Storage:** Parquet
- **Config:** YAML + Pydantic

## Development

```bash
# Lint & type-check (from athena-core)
ruff check src tests
mypy src
pytest
```

Pre-commit (optional):

```bash
pip install pre-commit
pre-commit install
pre-commit run --all-files
```

## License

MIT (pending formal LICENSE file)

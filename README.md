# StockMarketModel — Athena

**Athena** is an AI-powered Quantitative Research Operating System for discovering, validating, and explaining robust trading strategies on Indian equities (NSE / NIFTY 500, daily OHLCV).

This repository hosts the Athena monorepo under [`athena/`](athena/).

**Status:** MVP research loop complete (Phases 0–7). Rev 2 implementation adds portfolio, statistics, and pattern recognition MVPs — see [REV-2-IMPLEMENTATION-STATUS](athena/athena-spec/REV-2-IMPLEMENTATION-STATUS.md) and [Spec vs Code Status](athena/athena-spec/SPEC-VS-CODE-STATUS.md).

## Quick Start

**Requirements:** Python 3.11+

**One-command install (Windows):**

```powershell
.\athena\scripts\install.ps1
```

**Manual install:**

```bash
cd athena/athena-core
python -m venv .venv
.venv/Scripts/pip install -e ".[dev]"
.venv/Scripts/pip install -e "../athena-sdk[dev]" -e "../athena-cli[dev]" -e "../athena-dashboard[dev]" -e "../athena-ai[dev]"
.venv/Scripts/python -m pytest -q
```

Verify installation:

```bash
athena health
athena-ai "Find the best EMA strategy for sideways markets" --dry-run
```

### Phase-by-Phase Commands

| Phase | Package | Example |
|-------|---------|---------|
| **0–4** Core | `athena-core` | `pytest` in `athena-core` |
| **5** CLI / SDK / Dashboard | `athena-cli`, `athena-sdk`, `athena-dashboard` | `athena scan --strategy ... --as-of 2024-06-01` |
| **6** AI Assistant | `athena-ai` | `athena research "optimize ema parameters" --dry-run` |

```bash
# Scan with profile
athena scan --strategy athena/athena-examples/config/ema_crossover.yaml \
  --as-of 2024-06-01 --config athena/athena-examples/config/backtest.yaml \
  --profile paper --output scan.json

# Compare experiments
athena compare-experiments --latest 3 \
  --config athena/athena-examples/config/backtest.yaml --output-format table

# AI research (propose plan)
athena research "Find the best EMA strategy for sideways markets" \
  --config athena/athena-examples/config/backtest.yaml --dry-run

# Dashboard
athena-dashboard
```

## Documentation

Specifications live in [`athena/athena-spec/`](athena/athena-spec/README.md).

**Navigation tree:** [`ATHENA/`](athena/athena-spec/ATHENA/README.md) — Releases (REL-000…020), APS (Foundation + domains), ADR, Schemas, Golden Datasets, Benchmarks, Prompts, Reviews.

| Document | Purpose |
|----------|---------|
| [ATH-000 Philosophy](athena/athena-spec/ATH-000-Philosophy.md) | Mission and principles |
| [ATH-001 Vision & PRD](athena/athena-spec/ATH-001-Vision-PRD.md) | Product vision |
| [ATH-002 Engineering Standards](athena/athena-spec/ATH-002-Engineering-Standards.md) | Code quality rules |
| [ATH-REL-000 Engineering Standards](athena/athena-spec/ATH-REL-000-Engineering-Standards.md) | Release-00 master standards package (v0.1) |
| [ATH-REL-001 Core Framework](athena/athena-spec/ATH-REL-001-Core-Framework.md) | Release-01 core framework package (v0.1) |
| [ATH-003 Repository Architecture](athena/athena-spec/ATH-003-Repository-Architecture.md) | Monorepo layout |
| [Governance (AES)](athena/athena-spec/governance/) | Constitution, execution plan, quant & AI standards |
| [Definition of Done](athena/athena-spec/checklists/Definition-of-Done.md) | Deliverable checklist |
| [References Index](athena/athena-spec/REFERENCES-INDEX.md) | Package integration status (01–15 ✅) |
| [References Integration Complete](athena/athena-spec/REFERENCES-INTEGRATION-COMPLETE.md) | All 15 packages spec-integrated |
| [Spec vs Code Status](athena/athena-spec/SPEC-VS-CODE-STATUS.md) | Spec integration vs code implementation |
| [Rev 2 Implementation Status](athena/athena-spec/REV-2-IMPLEMENTATION-STATUS.md) | Portfolio, statistics, patterns MVPs |
| [ADRs](athena/athena-spec/adrs/) | Architecture decision records |
| [Decision Log](athena/athena-spec/decision-log/) | Delivery and process decisions |
| [Athena Handbook](athena/athena-docs/handbook/) | Operator volumes (Package 15) |
| [Requirements backlog](athena/athena-spec/requirements/) | Traceable REQ specs (hybrid layout) |
| [Platform Complete](athena/athena-spec/PLATFORM-COMPLETE.md) | MVP code sign-off (Phases 0–7) |
| [Phase 1 Foundation APS](athena/athena-spec/PHASE-1-FOUNDATION-COMPLETE.md) | ATHENA tree + APS-001…015 specs |
| [Phase 6 Validation](athena/athena-spec/PHASE-6-VALIDATION.md) | Latest phase validation report |
| [CHANGELOG](CHANGELOG.md) | Release history |

Redirect: [`Documents/`](Documents/README.md) → canonical [`athena/athena-spec/`](athena/athena-spec/README.md).

## Monorepo Layout

```
athena/
├── athena-spec/       # Specs, REQ backlog, validation reports
├── athena-core/       # Core library (Clean Architecture)
├── athena-ai/         # AI research assistant (NL experiment orchestration)
├── athena-sdk/        # Python SDK (AthenaClient)
├── athena-cli/        # Unified CLI (`athena`, `athena research`)
├── athena-dashboard/  # Streamlit MVP dashboard
├── athena-examples/   # Example strategies and configs
└── athena-docs/       # Handbook and documentation (Package 15)
```

## Phase Roadmap

| Phase | Focus | Status |
|-------|-------|--------|
| **0** | Monorepo scaffold, specs, REQ backlog | Complete |
| **1** | Data ingest, NSE calendar, EMA/SMA, feature store | Complete |
| **2** | Strategy YAML, backtest engine, experiment tracking | Complete |
| **3** | Walk-forward, optimizer, experiment comparison | Complete |
| **4** | Regime, ML scorer, scanner, explainability | Complete |
| **5** | Polished CLI, SDK, Streamlit dashboard | Complete |
| **6** | AI research assistant (`athena-ai`) | Complete |
| **7** | CI, install scripts, platform sign-off | Complete |

## MVP Defaults

- **Market:** NSE, NIFTY 500, daily OHLCV
- **Data source:** yfinance (MVP)
- **Storage:** Parquet
- **Config:** YAML + Pydantic

## Development

```bash
# Lint & test (from athena-core venv)
ruff check src tests
pytest

# Live integration tests (yfinance network)
pytest -m integration -v
```

CI runs on push/PR via GitHub Actions (`.github/workflows/ci.yml`).

Pre-commit (optional):

```bash
pip install pre-commit
pre-commit install
pre-commit run --all-files
```

## License

MIT — see [LICENSE](LICENSE).

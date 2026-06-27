# ATH-001 – MVP Scope

## Purpose
Define the minimum viable product for Athena Phase 1–2: a reproducible foundation for data, indicators, features, strategy configuration, and backtesting — before regime detection, ML, scanner, or dashboard.

## MVP Goal
Answer: *"Can I ingest NSE daily OHLCV, compute indicators, configure a rule-based strategy in YAML, backtest with realistic costs, and record a reproducible experiment?"*

## In Scope (MVP)

### Data Layer
- Daily OHLCV ingestion via yfinance for NIFTY 500 symbols
- Parquet storage with symbol/date partitioning
- NSE trading calendar (holidays, session boundaries)
- **REQ:** [REQ-DATA-INGEST-001](requirements/REQ-DATA-INGEST-001.md), [REQ-DATA-CALENDAR-001](requirements/REQ-DATA-CALENDAR-001.md)

### Indicators & Features
- Core trend indicators: EMA, SMA (vectorized, configurable periods)
- Feature store: persist computed features; skip recompute when available
- **REQ:** [REQ-IND-EMA-001](requirements/REQ-IND-EMA-001.md), [REQ-IND-SMA-001](requirements/REQ-IND-SMA-001.md), [REQ-FEAT-STORE-001](requirements/REQ-FEAT-STORE-001.md)

### Strategy & Backtest
- YAML-driven strategy schema (entry/exit rules, filters, position sizing, risk)
- No hardcoded strategy logic in `athena-core`
- Backtest engine with brokerage, slippage, taxes (configurable)
- Benchmark comparison (e.g. NIFTY 50 buy-and-hold)
- **REQ:** [REQ-STRAT-CONFIG-001](requirements/REQ-STRAT-CONFIG-001.md), [REQ-BT-ENGINE-001](requirements/REQ-BT-ENGINE-001.md)

### Experiment Tracking
- Metadata: strategy, version, dataset, periods, parameters, metrics, git commit, timestamp
- **REQ:** [REQ-EXP-TRACK-001](requirements/REQ-EXP-TRACK-001.md)

## Out of Scope (Future Phases)

| Capability | Target Phase | Notes |
|------------|--------------|-------|
| Corporate actions adjustment | Phase 2+ | MVP uses unadjusted OHLCV |
| Index membership history | Phase 2+ | Static NIFTY 500 list for MVP |
| Sector mapping | Phase 3+ | |
| 100+ feature library | Phase 2–3 | MVP: EMA, SMA + extensible store |
| Market regime engine | Phase 4 | Bull/bear/sideways classification |
| ML signal engine | Phase 5 | Scores strategy-generated signals |
| Explainability (SHAP) | Phase 5 | |
| Daily scanner | Phase 6 | Top trades, breakouts, RS ranking |
| Dashboard | Phase 7 | Web UI |
| Optimization engine | Phase 3 | Grid/random/Bayesian |
| AI research assistant | Future | Autonomous experiment orchestration |
| Live trading | Future | Research-only until validated |

## Technical Defaults (MVP)
- **Language:** Python 3.12+
- **Data source:** yfinance
- **Storage:** Parquet (local filesystem)
- **Config:** YAML + Pydantic validation
- **Architecture:** Clean Architecture in `athena-core` (domain / application / infrastructure / interfaces)

## MVP Success Criteria
1. Ingest ≥1 symbol and ≥1 year of daily OHLCV to Parquet
2. Compute EMA/SMA matching reference (pandas-ta)
3. Store and retrieve features without redundant recompute
4. Load a strategy from YAML and run a backtest with costs
5. Persist experiment metadata sufficient for reproduction
6. All REQ acceptance criteria met with passing unit tests

## Traceability
Every implementation PR must reference REQ IDs in commit messages and code docstrings where applicable (per ATH-002).

# AES-0203 – Repository Structure

> **Canonical layout:** [ATH-003-Repository-Architecture.md](../ATH-003-Repository-Architecture.md)  
> **References source:** `References/Athena-Package-02-Architecture/architecture/AES-0203-Repository-Structure.md`

Target and current monorepo structure. ATH-003 is canonical for day-to-day work; AES-0203 reconciles the References vision with the implemented layout.

---

## Current Monorepo (`athena/`)

```
athena/
├── athena-spec/           # Specifications, architecture, contracts, governance
│   ├── architecture/      # AES-0200–0203 (this package)
│   ├── contracts/         # Provider contracts
│   ├── diagrams/          # Mermaid architecture diagrams
│   ├── governance/        # AES-0001, 0002, 0005, 0006
│   ├── requirements/      # REQ backlog
│   ├── packages/          # Package integration validation reports
│   └── ...
├── athena-core/           # Core engine (domain, application, infrastructure, interfaces)
├── athena-ai/             # AI research assistant
├── athena-cli/            # Command-line interface
├── athena-sdk/            # Public Python SDK
├── athena-dashboard/      # Streamlit dashboard
├── athena-examples/       # Example strategies and configs
├── athena-docs/           # Future documentation site
└── Makefile               # install, test, lint
```

---

## References Target vs. Current

| References (AES-0203) | Current Status | Notes |
|-----------------------|----------------|-------|
| `athena-spec/` | ✅ | Extended with `architecture/`, `contracts/`, `diagrams/` |
| `athena-core/` | ✅ | MVP complete — data through ML in single package |
| `athena-market/` | ⏳ Deferred | Market intelligence lives in `athena-core/domain/regime` |
| `athena-research/` | ⏳ Deferred | Research in `athena-core/application/experiment_*` |
| `athena-ml/` | ⏳ Deferred | ML in `athena-core/application/ml_scorer` |
| `athena-ai/` | ✅ | Separate package (Phase 6) |
| `athena-dashboard/` | ✅ | Separate package (Phase 5) |
| `athena-sdk/` | ✅ | Separate package (Phase 5) |

Splitting `athena-market`, `athena-research`, and `athena-ml` into standalone packages is deferred until boundaries stabilize and import graphs justify extraction.

---

## `athena-core` Internal Structure

```
athena-core/src/athena_core/
├── domain/
│   ├── entities/          # OHLCVBar, Symbol
│   ├── indicators/        # EMA, SMA (pure functions)
│   ├── strategy/          # StrategyConfig, expression evaluator
│   ├── backtest/          # TradeRecord, PortfolioState
│   ├── regime/            # Regime models and indicators
│   ├── ports/             # Repository and store interfaces
│   └── plugins/           # PluginRegistry stub (AES-0202)
├── application/
│   ├── backtest_engine.py
│   ├── feature_service.py
│   ├── scanner.py
│   ├── optimizer.py
│   ├── experiment_tracker.py
│   ├── ml_scorer.py
│   └── runtime.py           # Composition root
├── infrastructure/
│   ├── parquet_ohlcv_store.py
│   ├── parquet_feature_store.py
│   ├── yfinance_client.py
│   ├── nse_calendar.py
│   └── strategy_yaml_loader.py
└── interfaces/
    └── cli.py
```

---

## Repository Root

```
StockMarketModel/
├── athena/                # Monorepo (above)
├── References/            # Read-only AES package sources (not edited)
├── Documents/             # Legacy spec copy — prefer athena-spec/
├── data/                  # Local OHLCV and feature data (gitignored)
└── README.md
```

---

## Related Documents

| Document | Purpose |
|----------|---------|
| [ATH-003 Repository Architecture](../ATH-003-Repository-Architecture.md) | Canonical monorepo description |
| [AES-0200 System Architecture](AES-0200-System-Architecture.md) | System layers |
| [AES-0201 Clean Architecture](AES-0201-Clean-Architecture.md) | Layer dependency rules |
| [PLATFORM-COMPLETE.md](../PLATFORM-COMPLETE.md) | MVP delivery status |

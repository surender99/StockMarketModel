# ATH-001 – Vision & Product Requirements

## Vision
Provide a professional quantitative research platform for retail traders — an institutional-grade research laboratory, not a simple backtesting application.

## Core Capabilities (Full Platform)
- Historical data ingestion
- Feature engineering (100+ features)
- Strategy engine (configuration-driven)
- Backtesting (walk-forward, costs, portfolio simulation)
- Portfolio simulation
- Optimization (grid, random, Bayesian, genetic)
- Machine learning (signal scoring, not trade creation)
- Explainable AI (SHAP, feature importance)
- Experiment tracking
- Research notebook
- Market regime detection
- Daily scanner (NIFTY 500 ranking)
- Dashboard (market overview, portfolio, research, reports)

See [ATH-001-MVP-Scope.md](ATH-001-MVP-Scope.md) for phased delivery.

## Target Market
- **Exchange:** NSE (National Stock Exchange of India)
- **Universe:** NIFTY 500 constituents
- **Bar frequency:** Daily OHLCV (MVP)

## Success Criteria
- Reproducible experiments (dataset version, git commit, parameters)
- Walk-forward validation
- Statistical robustness over maximum historical returns
- Explainable recommendations
- Every module independently replaceable (plugin-ready)

## Module Roadmap (from Vision)

| Phase | Modules | Status |
|-------|---------|--------|
| **MVP (Phase 1–2)** | Data layer, calendar, indicators (EMA/SMA), feature store, strategy config, backtest engine, experiment tracking | In progress |
| **Phase 3** | Extended indicators, portfolio engine, optimization | Planned |
| **Phase 4** | Market regime engine | Planned |
| **Phase 5** | ML signal engine, explainability | Planned |
| **Phase 6** | Daily scanner | Planned |
| **Phase 7** | Dashboard, APIs, live trading hooks | Planned |
| **Future** | AI research assistant | Planned |

## Related Documents
- [ATH-001-MVP-Scope.md](ATH-001-MVP-Scope.md)
- [requirements/](requirements/)
- [ATH-003-Repository-Architecture.md](ATH-003-Repository-Architecture.md)

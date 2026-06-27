# ATH-003 – Repository Architecture

```
athena/
├── athena-spec/       # Specifications, REQ backlog, validation reports
├── athena-core/       # Clean Architecture: domain, application, infrastructure, interfaces
├── athena-ai/         # Future: AI research assistant
├── athena-docs/       # Future: user/developer documentation site
├── athena-sdk/        # Future: public Python SDK
├── athena-cli/        # Future: command-line interface
└── athena-examples/   # Future: example strategies and notebooks
```

## Core Modules (athena-core)
- Data
- Feature Store
- Indicators
- Strategies
- Backtester
- Portfolio
- Optimizer
- ML
- Dashboard
- APIs

MVP implements: Data, Calendar, Indicators, Feature Store, Strategy Config, Backtester, Experiment Tracking.

## Clean Architecture Layers (athena-core)

| Layer | Responsibility |
|-------|----------------|
| `domain/` | Entities, value objects, domain interfaces — no I/O |
| `application/` | Use cases, orchestration — depends on domain only |
| `infrastructure/` | yfinance, Parquet, logging, file I/O |
| `interfaces/` | CLI, future REST/API adapters |

Dependencies point inward: interfaces → application → domain; infrastructure implements domain ports.

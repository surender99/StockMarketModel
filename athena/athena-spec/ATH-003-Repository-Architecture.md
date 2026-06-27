# ATH-003 – Repository Architecture

> **Architecture specs:** [architecture/](architecture/) (AES-0200–0203)  
> **Provider contracts:** [contracts/](contracts/)  
> **System diagram:** [diagrams/system-layer.mmd](diagrams/system-layer.mmd)

```
athena/
├── athena-spec/       # Specifications, REQ backlog, validation reports
│   ├── architecture/  # AES-0200–0203 system, clean, plugin, repo structure
│   ├── contracts/     # IndicatorProvider, StrategyProvider
│   └── diagrams/      # Mermaid architecture diagrams
├── athena-core/       # Clean Architecture: domain, application, infrastructure, interfaces
├── athena-ai/         # AI research assistant
├── athena-cli/        # Command-line interface
├── athena-sdk/        # Public Python SDK
├── athena-dashboard/  # Streamlit dashboard
├── athena-docs/       # Future: user/developer documentation site
└── athena-examples/   # Example strategies and configs
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

See [AES-0201 Clean Architecture](architecture/AES-0201-Clean-Architecture.md) for the full dependency matrix and port mapping.

## System Architecture

Athena is organized into 13 system layers (governance through platform). Lower layers never depend on higher layers; all cross-layer communication uses documented contracts.

| Document | Purpose |
|----------|---------|
| [AES-0200 System Architecture](architecture/AES-0200-System-Architecture.md) | Layer model and data flow |
| [AES-0202 Plugin Architecture](architecture/AES-0202-Plugin-Architecture.md) | Plugin contract and registry |
| [AES-0203 Repository Structure](architecture/AES-0203-Repository-Structure.md) | Target vs. current package layout |
| [IndicatorProvider](contracts/IndicatorProvider.md) | Indicator plugin contract |
| [StrategyProvider](contracts/StrategyProvider.md) | Strategy plugin contract |

# AES-0200 – System Architecture

> **Canonical repo layout:** [ATH-003-Repository-Architecture.md](../ATH-003-Repository-Architecture.md)  
> **References source:** `References/Athena-Package-02-Architecture/architecture/AES-0200-System-Architecture.md`  
> **Diagram:** [system-layer.mmd](../diagrams/system-layer.mmd)

Defines the complete Athena system architecture — layers, dependency rules, and communication boundaries.

---

## Purpose

Athena is a layered quantitative research operating system. Each layer has a single responsibility and exposes capabilities only through documented contracts (ports and providers). Lower layers never depend on higher layers.

---

## System Layers

| # | Layer | Responsibility | MVP Status |
|---|-------|----------------|------------|
| 1 | **Governance** | Constitution, standards, execution plan, DoD | ✅ [governance/](../governance/) |
| 2 | **Data** | OHLCV ingest, storage, calendar | ✅ `athena-core` infrastructure |
| 3 | **Market Intelligence** | Regime, breadth, relative strength | ✅ Regime engine (partial) |
| 4 | **Feature Store** | Cached indicator/feature materialization | ✅ Parquet feature store |
| 5 | **Indicators** | Pure, vectorized technical features | ✅ EMA, SMA |
| 6 | **Pattern Recognition** | Chart and candlestick events | ⏳ Package 06 |
| 7 | **Strategy Engine** | Entry/exit/risk rules → signals | ✅ YAML `StrategyConfig` |
| 8 | **Backtester** | Event-driven simulation, metrics | ✅ `BacktestEngine` |
| 9 | **Portfolio** | Position sizing, exposure | ✅ In backtest engine |
| 10 | **Research** | Experiments, walk-forward, compare | ✅ Experiment tracker |
| 11 | **ML** | Signal scoring, explainability | ✅ ML scorer, SHAP |
| 12 | **AI** | Research assistant, intent parsing | ✅ `athena-ai` |
| 13 | **Platform** | CLI, SDK, dashboard, CI | ✅ Phases 5–7 |

---

## Architecture Rules

1. **Lower layers never depend on higher layers** — e.g. `domain/indicators` must not import from `application/backtest_engine`.
2. **All cross-layer communication through interfaces** — domain ports (`OHLCVRepositoryPort`, `FeatureStorePort`), application ports (`FeatureProviderPort`), and provider contracts ([contracts/](../contracts/)).
3. **Plugin-first architecture** — indicators, patterns, strategies, and ML models register via the plugin model ([AES-0202](AES-0202-Plugin-Architecture.md)).
4. **Configuration over hardcoding** — strategies, backtests, and experiments are YAML-driven ([ATH-000](../ATH-000-Philosophy.md)).

---

## Data Flow (Research Loop)

See [system-layer.mmd](../diagrams/system-layer.mmd) for the canonical layer flow:

```
Historical Data → Market Intelligence → Feature Store → Indicators
  → Strategy Engine → Backtester → Portfolio → Research → ML → AI
```

MVP implements the core loop end-to-end: ingest → features → strategy → backtest → experiment tracking → AI-assisted research.

---

## Package Boundaries

| Package | Role |
|---------|------|
| `athena-spec` | Specifications, architecture, contracts, REQ backlog |
| `athena-core` | Domain, application, infrastructure, interfaces (layers 2–11 core) |
| `athena-ai` | AI research assistant (layer 12) |
| `athena-cli` | Command-line platform interface |
| `athena-sdk` | Public Python SDK |
| `athena-dashboard` | Streamlit visualization |
| `athena-examples` | Example strategies and configs |
| `athena-docs` | Future documentation site |

Future packages (`athena-market`, `athena-research`, `athena-ml`) may split from `athena-core` as the platform scales — see [AES-0203](AES-0203-Repository-Structure.md).

---

## Related Documents

| Document | Purpose |
|----------|---------|
| [ATH-003 Repository Architecture](../ATH-003-Repository-Architecture.md) | Canonical monorepo layout and core modules |
| [AES-0201 Clean Architecture](AES-0201-Clean-Architecture.md) | Dependency rule and layer mapping |
| [AES-0202 Plugin Architecture](AES-0202-Plugin-Architecture.md) | Plugin contract and registry |
| [AES-0203 Repository Structure](AES-0203-Repository-Structure.md) | Target vs. current package layout |
| [IndicatorProvider](../contracts/IndicatorProvider.md) | Indicator contract |
| [StrategyProvider](../contracts/StrategyProvider.md) | Strategy contract |
| [PLATFORM-COMPLETE.md](../PLATFORM-COMPLETE.md) | MVP sign-off |

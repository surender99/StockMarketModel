# References Package Integration Index

> **Canonical spec:** `athena/athena-spec/`
> **Read-only source:** `References/Athena-Package-NN-*/`
> **Integration complete:** [REFERENCES-INTEGRATION-COMPLETE.md](REFERENCES-INTEGRATION-COMPLETE.md)

This index tracks integration of the Athena References package series and Release-00 artifacts into the monorepo specification.

---

## Status Overview

| Package | Name | Scope | Status |
|---------|------|-------|--------|
| **REL-000** | Engineering Standards (Release-00) | Master standards taxonomy, quality gates, section index | ✅ Complete |
| **REL-001** | Core Framework (Release-01) | Config, DI, plugins, events, logging, errors, utilities, contracts | ✅ Complete |
| **REL-002** | Data Platform (Release-02) | Historical/live data, instrument master, validation, versioning | ✅ Complete |
| **REL-003** | Feature Engineering (Release-03) | Indicator registry, pipeline, cache policies, ATR/ADX/Bollinger | ✅ Complete |
| **REL-002** | Data Platform (Release-02) | OHLCV ingest, calendar, quality, cleaning, versioning, registry | ✅ Complete |
| **01** | Governance | Constitution, execution plan, quant & AI standards, templates, DoD | ✅ Complete |
| **02** | Architecture | System architecture, clean architecture, plugin model, repo structure | ✅ Complete |
| **03** | Data Platform | DataProvider contract, OHLCV schema, data quality | ✅ Complete |
| **04** | Market Intelligence | Regime, breadth, relative strength, sector rotation | ✅ Complete |
| **05** | Feature Engineering | Indicator framework, indicator catalog, MACD/RSI | ✅ Complete |
| **06** | Pattern Recognition | Chart and candlestick patterns, PatternProvider | ✅ Complete |
| **07** | Strategy Engine | Strategy DSL, lifecycle, StrategyProvider | ✅ Complete |
| **08** | Backtesting | Backtester contract, execution model, metrics | ✅ Complete |
| **09** | Portfolio Engine | Portfolio provider, risk management | ✅ Complete |
| **10** | Research Engine | Experiment lifecycle, ResearchProvider | ✅ Complete |
| **11** | Statistics | Validation framework, core metrics | ✅ Complete |
| **12** | Machine Learning | ML lifecycle, training pipeline | ✅ Complete |
| **13** | AI Research Scientist | Knowledge memory, review workflows | ✅ Complete |
| **14** | Platform | Production platform framework | ✅ Complete |
| **15** | Handbook | Operator volumes and reference books | ✅ Complete |

---

## Package Artifact Map

| Pkg | Canonical Path | Validation |
|-----|----------------|------------|
| REL-000 | [ATH-REL-000-Engineering-Standards.md](ATH-REL-000-Engineering-Standards.md), [engineering-standards/](engineering-standards/) | [PACKAGE-REL-000-COMPLETE.md](packages/PACKAGE-REL-000-COMPLETE.md) |
| REL-001 | [ATH-REL-001-Core-Framework.md](ATH-REL-001-Core-Framework.md), [release-01/](release-01/) | [PACKAGE-REL-001-COMPLETE.md](packages/PACKAGE-REL-001-COMPLETE.md) |
| REL-002 | [ATH-REL-002-Data-Platform.md](ATH-REL-002-Data-Platform.md), [release-02/](release-02/) | [PACKAGE-REL-002-COMPLETE.md](packages/PACKAGE-REL-002-COMPLETE.md) |
| REL-003 | [ATH-REL-003-Feature-Engineering.md](ATH-REL-003-Feature-Engineering.md), [release-03/](release-03/) | [PACKAGE-REL-003-COMPLETE.md](packages/PACKAGE-REL-003-COMPLETE.md) |
| REL-002 | [ATH-REL-002-Data-Platform.md](ATH-REL-002-Data-Platform.md), [release-02/](release-02/) | [PACKAGE-REL-002-COMPLETE.md](packages/PACKAGE-REL-002-COMPLETE.md) |
| 01 | [governance/](governance/), [templates/](templates/), [checklists/](checklists/) | [PACKAGE-01-COMPLETE.md](packages/PACKAGE-01-COMPLETE.md) |
| 02 | [architecture/](architecture/), [contracts/](contracts/), [diagrams/](diagrams/) | [PACKAGE-02-COMPLETE.md](packages/PACKAGE-02-COMPLETE.md) |
| 03 | [data/](data/), [schemas/ohlcv-schema.json](schemas/ohlcv-schema.json), [DataProvider](contracts/DataProvider.md) | [PACKAGE-03-COMPLETE.md](packages/PACKAGE-03-COMPLETE.md) |
| 04 | [market-intelligence/](market-intelligence/) | [PACKAGE-04-COMPLETE.md](packages/PACKAGE-04-COMPLETE.md) |
| 05 | [feature-engineering/](feature-engineering/) | [PACKAGE-05-COMPLETE.md](packages/PACKAGE-05-COMPLETE.md) |
| 06 | [pattern-recognition/](pattern-recognition/) | [PACKAGE-06-COMPLETE.md](packages/PACKAGE-06-COMPLETE.md) |
| 07 | [strategy-engine/](strategy-engine/) | [PACKAGE-07-COMPLETE.md](packages/PACKAGE-07-COMPLETE.md) |
| 08 | [backtesting/](backtesting/) | [PACKAGE-08-COMPLETE.md](packages/PACKAGE-08-COMPLETE.md) |
| 09 | [portfolio-engine/](portfolio-engine/) | [PACKAGE-09-COMPLETE.md](packages/PACKAGE-09-COMPLETE.md) |
| 10 | [research-engine/](research-engine/) | [PACKAGE-10-COMPLETE.md](packages/PACKAGE-10-COMPLETE.md) |
| 11 | [statistics/](statistics/) | [PACKAGE-11-COMPLETE.md](packages/PACKAGE-11-COMPLETE.md) |
| 12 | [machine-learning/](machine-learning/) | [PACKAGE-12-COMPLETE.md](packages/PACKAGE-12-COMPLETE.md) |
| 13 | [ai-research/](ai-research/) | [PACKAGE-13-COMPLETE.md](packages/PACKAGE-13-COMPLETE.md) |
| 14 | [platform/](platform/) | [PACKAGE-14-COMPLETE.md](packages/PACKAGE-14-COMPLETE.md) |
| 15 | [athena-docs/handbook/](../athena-docs/handbook/) | [PACKAGE-15-COMPLETE.md](packages/PACKAGE-15-COMPLETE.md) |

---

## Integration Rules

1. **References/ is read-only** — never edit source packages; integrate into `athena-spec`.
2. **Avoid duplication** — cross-link ATH docs when they already cover AES content.
3. **Preserve AES IDs** — keep `AES-NNNN` numbering for traceability.
4. **One package at a time** — complete validation report before starting the next package.

---

## Related Documents

- [README.md](README.md) — spec reading order
- [PLATFORM-COMPLETE.md](PLATFORM-COMPLETE.md) — MVP code sign-off (Phases 0–7)
- [REFERENCES-INTEGRATION-COMPLETE.md](REFERENCES-INTEGRATION-COMPLETE.md) — spec integration sign-off
- [SPEC-VS-CODE-STATUS.md](SPEC-VS-CODE-STATUS.md) — spec vs implementation gaps
- [adrs/](adrs/) — architecture decision records
- [decision-log/](decision-log/) — delivery and process decisions

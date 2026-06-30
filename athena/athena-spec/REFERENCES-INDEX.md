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
| **REL-004** | Indicator Framework (Release-04) | Indicator engine, WMA/ROC/OBV/CMF/MFI/CCI/Williams %R, validation | ✅ Complete |
| **REL-005** | Pattern Recognition (Release-05) | PatternProvider registry, expanded candlestick/chart catalog | ✅ Complete |
| **REL-006** | Strategy Engine (Release-06) | Strategy registry, signal engine, composition, validation, sizing | ✅ Complete |
| **REL-007** | Backtesting Engine (Release-07) | Order engine, execution models, slippage, trade journal, advanced metrics | ✅ Complete |
| **REL-008** | Portfolio Management Engine (Release-08) | Allocation models, risk budgets, optimization, analytics, snapshots | ✅ Complete |
| **REL-009** | Statistics & Analytics Engine (Release-09) | Distribution, hypothesis tests, correlation, regression, reporting | ✅ Complete |
| **REL-010** | Research Engine (Release-10) | Research workspace, experiment lifecycle, dataset snapshots, pipeline, results | ✅ Complete — **Phase 9 QREP APS** |
| **REL-011** | Machine Learning Platform (Release-11) | Feature selection, dataset builder, model registry, training, evaluation, drift | ✅ Complete |
| **REL-012** | AI Research Scientist (Release-12) | AI planner, hypothesis generator, strategy designer, reviewer, docs | ✅ Complete |
| **REL-013** | Dashboard & Visualization (Release-13) | Chart engine, portfolio/strategy/risk/research dashboards | ✅ Complete |
| **REL-014** | Paper Trading Engine (Release-14) | Paper broker, orders, positions, execution simulator, risk controls | ✅ Complete |
| **REL-015** | Production & Deployment (Release-15) | Broker gateway, OMS, RMS, health checks, audit logging | ✅ Complete |
| **REL-016** | Engineering Review Framework (Release-16) | Architecture/code/quant reviews, release gates | ✅ Complete |
| **REL-017** | Security & Compliance (Release-17) | Authentication, RBAC, secrets, audit trails | ✅ Complete |
| **REL-018** | DevOps & Platform Engineering (Release-18) | CI/CD, artifacts, deployment pipelines | ✅ Complete |
| **REL-019** | Observability & Monitoring (Release-19) | Metrics, tracing, alerting, SLA/SLO reporting | ✅ Complete |
| **REL-020** | SDK & Public APIs (Release-20) | Python SDK, REST/WS stubs, rate limiting, API versioning | ✅ Complete |
| **ATH-000A** | Core Architecture | Vision, layers, AthenaOS, dependency rules | ✅ Complete |
| **ATH-000B** | Engineering Standards (extended) | Coding, naming, testing, DoD, AI agent rules | ✅ Complete |
| **ATH-000C** | Contracts, Events & APIs | Interface/DTO/event/API standards, templates | ✅ Complete |
| **ATH-000D** | AI Governance & Quality | AI coding, reviews, quality gates, release governance | ✅ Complete |
| **ATH-001** | AthenaOS Runtime | Module model, service lifecycle, extension points | ✅ Complete |
| **ATH-002** | Dependency Graph | Layering policy, dependency matrix, build integration | ✅ Complete |
| **ATH-003** | Master Event Catalog | Event naming, versioning, governance standards | ✅ Complete |
| **ATH-004** | Master Interface Catalog | Interface principles, DTO ownership, compatibility | ✅ Complete |
| **ATH-005** | Master Database Catalog | Schema catalog, migrations, audit standards | ✅ Complete |
| **ATH-IP** | Implementation Starter Pack | EventBus, WorkflowEngine, PluginRegistry IPs | ✅ Complete |
| **PHASE 10** | Machine Learning Platform (MLP) | 148 APS — training, registry, drift, prediction | ✅ Complete |
| **PHASE 11** | Autonomous Quant Intelligence (AQIP) | 110 APS — multi-agent research orchestration | ✅ Complete |
| **PHASE 12** | Visualization & UX (VDSUX) | 106 APS — dashboards, charts, decision support | ✅ Complete |
| **PHASE 13** | Paper Trading (PTEVP) | 85 APS — paper broker, live feed, validation | ✅ Complete |
| **PHASE 14** | Enterprise Trading (ETOP) | 102 APS — OMS, RMS, broker gateway | ✅ Complete |
| **PHASE 15** | Enterprise Governance (EGPCI) | 91 APS — platform engineering, CI/CD, observability | ✅ Complete |
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
| REL-004 | [ATH-REL-004-Indicator-Framework.md](ATH-REL-004-Indicator-Framework.md), [release-04/](release-04/) | [PACKAGE-REL-004-COMPLETE.md](packages/PACKAGE-REL-004-COMPLETE.md) |
| REL-005 | [ATH-REL-005-Pattern-Recognition.md](ATH-REL-005-Pattern-Recognition.md), [release-05/](release-05/) | [PACKAGE-REL-005-COMPLETE.md](packages/PACKAGE-REL-005-COMPLETE.md) |
| REL-006 | [ATH-REL-006-Strategy-Engine.md](ATH-REL-006-Strategy-Engine.md), [release-06/](release-06/) | [PACKAGE-REL-006-COMPLETE.md](packages/PACKAGE-REL-006-COMPLETE.md) |
| REL-007 | [ATH-REL-007-Backtesting-Engine.md](ATH-REL-007-Backtesting-Engine.md), [release-07/](release-07/) | [PACKAGE-REL-007-COMPLETE.md](packages/PACKAGE-REL-007-COMPLETE.md) |
| REL-008 | [ATH-REL-008-Portfolio-Management-Engine.md](ATH-REL-008-Portfolio-Management-Engine.md), [release-08/](release-08/) | [PACKAGE-REL-008-COMPLETE.md](packages/PACKAGE-REL-008-COMPLETE.md) |
| REL-009 | [ATH-REL-009-Statistics-and-Analytics-Engine.md](ATH-REL-009-Statistics-and-Analytics-Engine.md), [release-09/](release-09/) | [PACKAGE-REL-009-COMPLETE.md](packages/PACKAGE-REL-009-COMPLETE.md) |
| REL-010 | [ATH-REL-010-Research-Engine.md](ATH-REL-010-Research-Engine.md), [release-10/](release-10/) | [PACKAGE-REL-010-COMPLETE.md](packages/PACKAGE-REL-010-COMPLETE.md) |
| REL-011 | [ATH-REL-011-Machine-Learning-Platform.md](ATH-REL-011-Machine-Learning-Platform.md), [release-11/](release-11/) | [PACKAGE-REL-011-COMPLETE.md](packages/PACKAGE-REL-011-COMPLETE.md) |
| REL-012 | [ATH-REL-012-AI-Research-Scientist.md](ATH-REL-012-AI-Research-Scientist.md), [release-12/](release-12/) | [PACKAGE-REL-012-COMPLETE.md](packages/PACKAGE-REL-012-COMPLETE.md) |
| REL-013 | [ATH-REL-013-Dashboard-and-Visualization.md](ATH-REL-013-Dashboard-and-Visualization.md), [release-13/](release-13/) | [PACKAGE-REL-013-COMPLETE.md](packages/PACKAGE-REL-013-COMPLETE.md) |
| REL-014 | [ATH-REL-014-Paper-Trading-Engine.md](ATH-REL-014-Paper-Trading-Engine.md), [release-14/](release-14/) | [PACKAGE-REL-014-COMPLETE.md](packages/PACKAGE-REL-014-COMPLETE.md) |
| REL-015 | [ATH-REL-015-Production-and-Deployment.md](ATH-REL-015-Production-and-Deployment.md), [release-15/](release-15/) | [PACKAGE-REL-015-COMPLETE.md](packages/PACKAGE-REL-015-COMPLETE.md) |
| REL-016 | [ATH-REL-016-Engineering-Review-Framework.md](ATH-REL-016-Engineering-Review-Framework.md), [release-16/](release-16/) | [PACKAGE-REL-016-COMPLETE.md](packages/PACKAGE-REL-016-COMPLETE.md) |
| REL-017 | [ATH-REL-017-Security-and-Compliance.md](ATH-REL-017-Security-and-Compliance.md), [release-17/](release-17/) | [PACKAGE-REL-017-COMPLETE.md](packages/PACKAGE-REL-017-COMPLETE.md) |
| REL-018 | [ATH-REL-018-DevOps-and-Platform-Engineering.md](ATH-REL-018-DevOps-and-Platform-Engineering.md), [release-18/](release-18/) | [PACKAGE-REL-018-COMPLETE.md](packages/PACKAGE-REL-018-COMPLETE.md) |
| REL-019 | [ATH-REL-019-Observability-and-Monitoring.md](ATH-REL-019-Observability-and-Monitoring.md), [release-19/](release-19/) | [PACKAGE-REL-019-COMPLETE.md](packages/PACKAGE-REL-019-COMPLETE.md) |
| REL-020 | [ATH-REL-020-SDK-and-Public-APIs.md](ATH-REL-020-SDK-and-Public-APIs.md), [release-20/](release-20/) | [PACKAGE-REL-020-COMPLETE.md](packages/PACKAGE-REL-020-COMPLETE.md) |
| ATH-000A | [ATHENA/Architecture/](ATHENA/Architecture/00-README.md) | [ATH-000-SERIES-INDEX.md](ATH-000-SERIES-INDEX.md) |
| ATH-000B | [engineering-standards/ATH-000B/](engineering-standards/ATH-000B/00-README.md) | [ATH-000-SERIES-INDEX.md](ATH-000-SERIES-INDEX.md) |
| ATH-000C | [ATHENA/Contracts-Standards/](ATHENA/Contracts-Standards/00-README.md) | [ATH-000-SERIES-INDEX.md](ATH-000-SERIES-INDEX.md) |
| ATH-000D | [governance/ATH-000D/](governance/ATH-000D/00-README.md) | [ATH-000-SERIES-INDEX.md](ATH-000-SERIES-INDEX.md) |
| ATH-001 | [ATHENA/AthenaOS/](ATHENA/AthenaOS/00-README.md) | [ATH-001-SERIES-INDEX.md](ATH-001-SERIES-INDEX.md) |
| ATH-002 | [ATHENA/Dependency-Graph/](ATHENA/Dependency-Graph/00-README.md) | [ATH-001-SERIES-INDEX.md](ATH-001-SERIES-INDEX.md) |
| ATH-003 | [events/](events/00-README.md) | [ATH-001-SERIES-INDEX.md](ATH-001-SERIES-INDEX.md) |
| ATH-004 | [interfaces/](interfaces/00-README.md) | [ATH-001-SERIES-INDEX.md](ATH-001-SERIES-INDEX.md) |
| ATH-005 | [database/](database/00-README.md) | [ATH-001-SERIES-INDEX.md](ATH-001-SERIES-INDEX.md) |
| ATH-IP | [implementation-packages/ATH-IP-Starter-Pack/](implementation-packages/ATH-IP-Starter-Pack/README.md) | [ATH-001-SERIES-COMPLETE.md](ATH-001-SERIES-COMPLETE.md) |
| PHASE 10 | [ATHENA/APS/Machine-Learning/](ATHENA/APS/Machine-Learning/README.md) | [PHASE-10-MLP-COMPLETE.md](PHASE-10-MLP-COMPLETE.md) |
| PHASE 11 | [ATHENA/APS/Autonomous-Intelligence/](ATHENA/APS/Autonomous-Intelligence/README.md) | [PHASE-11-AQIP-COMPLETE.md](PHASE-11-AQIP-COMPLETE.md) |
| PHASE 12 | [ATHENA/APS/Visualization-UX/](ATHENA/APS/Visualization-UX/README.md) | [PHASE-12-VDSUX-COMPLETE.md](PHASE-12-VDSUX-COMPLETE.md) |
| PHASE 13 | [ATHENA/APS/Paper-Trading/](ATHENA/APS/Paper-Trading/README.md) | [PHASE-13-PTEVP-COMPLETE.md](PHASE-13-PTEVP-COMPLETE.md) |
| PHASE 14 | [ATHENA/APS/Enterprise-Trading/](ATHENA/APS/Enterprise-Trading/README.md) | [PHASE-14-ETOP-COMPLETE.md](PHASE-14-ETOP-COMPLETE.md) |
| PHASE 15 | [ATHENA/APS/Enterprise-Governance/](ATHENA/APS/Enterprise-Governance/README.md) | [PHASE-15-EGPCI-COMPLETE.md](PHASE-15-EGPCI-COMPLETE.md) |
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
| 10 | [research-engine/](research-engine/), [Research-Experimentation APS](ATHENA/APS/Research-Experimentation/README.md) | [PACKAGE-10-COMPLETE.md](packages/PACKAGE-10-COMPLETE.md), [PHASE-9-QREP-COMPLETE.md](PHASE-9-QREP-COMPLETE.md) |
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

## Architecture Packages (2026-06-30)

| Package | Path | ADR | Status |
|---------|------|-----|--------|
| **ATH-001 AthenaOS** | [ATHENA/AthenaOS/](ATHENA/AthenaOS/00-README.md) | [ADR-0005](adrs/ADR-0005-athena-os.md) | ✅ Spec + MVP code |
| **ATH-002 Dependency Graph** | [ATHENA/Dependency-Graph/](ATHENA/Dependency-Graph/00-README.md) | — | ✅ Spec integrated |
| **ATH-003 Event Catalog** | [events/](events/00-README.md) | — | ✅ Standards + 20 wired events |
| **ATH-004 Interface Catalog** | [interfaces/](interfaces/00-README.md) | — | ✅ Standards + 23 interfaces |
| **ATH-005 Database Catalog** | [database/](database/00-README.md) | — | ✅ Spec integrated |
| **ATH-IP Starter Pack** | [implementation-packages/](implementation-packages/ATH-IP-Starter-Pack/README.md) | — | ✅ 3 starter IPs |
| **athena-os** | `athena/athena-os/` | [ADR-0005](adrs/ADR-0005-athena-os.md) | ✅ MVP — infrastructure layer |
| **athena-testing** | `athena/athena-testing/` | — | ✅ MVP — golden datasets, benchmarks |
| **APS traceability** | `ATHENA/APS/TRACEABILITY-INDEX.md` | [ATH-005](ATH-005-DOCUMENTATION-STANDARD.md) | ✅ Template + 12 sample APS |

---

## Related Documents

- [README.md](README.md) — spec reading order
- [ATHENA/README.md](ATHENA/README.md) — APS traceability and package map
- [ATHENA/DEPENDENCY-RULES.md](ATHENA/DEPENDENCY-RULES.md) — package dependency enforcement
- [ATH-005-DOCUMENTATION-STANDARD.md](ATH-005-DOCUMENTATION-STANDARD.md) — per-feature documentation requirements
- [PLATFORM-COMPLETE.md](PLATFORM-COMPLETE.md) — MVP code sign-off (Phases 0–9)
- [REFERENCES-INTEGRATION-COMPLETE.md](REFERENCES-INTEGRATION-COMPLETE.md) — spec integration sign-off
- [SPEC-VS-CODE-STATUS.md](SPEC-VS-CODE-STATUS.md) — spec vs implementation gaps
- [adrs/](adrs/) — architecture decision records
- [decision-log/](decision-log/) — delivery and process decisions

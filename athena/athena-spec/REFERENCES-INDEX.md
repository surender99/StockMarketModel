# References Package Integration Index

> **Canonical spec:** `athena/athena-spec/`  
> **Read-only source:** `References/Athena-Package-NN-*/`

This index tracks integration of the Athena References package series into the monorepo specification.

---

## Status Overview

| Package | Name | Scope | Status |
|---------|------|-------|--------|
| **01** | Governance | Constitution, execution plan, quant & AI standards, templates, DoD | ✅ Complete |
| **02** | Architecture | System architecture, clean architecture, plugin model, repo structure | ✅ Complete |
| **03** | Data Platform | DataProvider contract, OHLCV schema, data quality | ⏳ Pending |
| **04** | Market Intelligence | Regime, breadth, relative strength, sector rotation | ⏳ Pending |
| **05** | Feature Engineering | Indicator framework, indicator catalog | ⏳ Pending |
| **06** | Pattern Recognition | Chart and candlestick patterns, PatternProvider | ⏳ Pending |
| **07** | Strategy Engine | Strategy DSL, lifecycle, StrategyProvider | ⏳ Pending |
| **08** | Backtesting | Backtester contract, execution model, metrics | ⏳ Pending |
| **09** | Portfolio Engine | Portfolio provider, risk management | ⏳ Pending |
| **10** | Research Engine | Experiment lifecycle, ResearchProvider | ⏳ Pending |
| **11** | Statistics | Validation framework, core metrics | ⏳ Pending |
| **12** | Machine Learning | ML lifecycle, training pipeline | ⏳ Pending |
| **13** | AI Research Scientist | Knowledge memory, review workflows | ⏳ Pending |
| **14** | Platform | Production platform framework | ⏳ Pending |
| **15** | Handbook | Operator volumes and reference books | ⏳ Pending |

---

## Package 01 — Integrated Artifacts

| Source (References) | Canonical (athena-spec) | Notes |
|---------------------|-------------------------|-------|
| AES-0001 Constitution | [governance/AES-0001-Constitution.md](governance/AES-0001-Constitution.md) | Cross-links [ATH-000](ATH-000-Philosophy.md) |
| AES-0002 Master Execution Plan | [governance/AES-0002-Master-Execution-Plan.md](governance/AES-0002-Master-Execution-Plan.md) | Mapped to Phases 0–7 |
| AES-0003 Vision | [ATH-001-Vision-PRD.md](ATH-001-Vision-PRD.md) | Not duplicated — ATH-001 is canonical |
| AES-0004 Engineering Standards | [ATH-002-Engineering-Standards.md](ATH-002-Engineering-Standards.md) | Merged via cross-links |
| AES-0005 Quant Standards | [governance/AES-0005-Quant-Standards.md](governance/AES-0005-Quant-Standards.md) | New — ATH had no quant doc |
| AES-0006 AI Coding Standards | [governance/AES-0006-AI-Coding-Standards.md](governance/AES-0006-AI-Coding-Standards.md) | Enriches ATH-002 |
| Roadmap | [AES-0002](governance/AES-0002-Master-Execution-Plan.md) | Sprint table |
| Definition of Done | [checklists/Definition-of-Done.md](checklists/Definition-of-Done.md) | Extended for package integration |
| ADR / RFC / Requirement templates | [templates/](templates/) | ATH-004-aligned |
| AI Implementation Prompt | [prompts/AI-Implementation-Prompt.md](prompts/AI-Implementation-Prompt.md) | Agent workflow |

**Validation report:** [packages/PACKAGE-01-COMPLETE.md](packages/PACKAGE-01-COMPLETE.md)

---

## Package 02 — Integrated Artifacts

| Source (References) | Canonical (athena-spec) | Notes |
|---------------------|-------------------------|-------|
| AES-0200 System Architecture | [architecture/AES-0200-System-Architecture.md](architecture/AES-0200-System-Architecture.md) | Enriched with MVP layer status |
| AES-0201 Clean Architecture | [architecture/AES-0201-Clean-Architecture.md](architecture/AES-0201-Clean-Architecture.md) | Port/adapter mapping to athena-core |
| AES-0202 Plugin Architecture | [architecture/AES-0202-Plugin-Architecture.md](architecture/AES-0202-Plugin-Architecture.md) | `PluginRegistry` stub in athena-core |
| AES-0203 Repository Structure | [architecture/AES-0203-Repository-Structure.md](architecture/AES-0203-Repository-Structure.md) | Reconciled with current monorepo |
| IndicatorProvider | [contracts/IndicatorProvider.md](contracts/IndicatorProvider.md) | Aligned with `FeatureService` registry |
| StrategyProvider | [contracts/StrategyProvider.md](contracts/StrategyProvider.md) | Aligned with `StrategyConfig` |
| system-layer.mmd | [diagrams/system-layer.mmd](diagrams/system-layer.mmd) | Canonical data-flow diagram |
| ATH-003 | [ATH-003-Repository-Architecture.md](ATH-003-Repository-Architecture.md) | Cross-links added; remains canonical |

**Validation report:** [packages/PACKAGE-02-COMPLETE.md](packages/PACKAGE-02-COMPLETE.md)

---

## Integration Rules

1. **References/ is read-only** — never edit source packages; integrate into `athena-spec`.
2. **Avoid duplication** — cross-link ATH docs when they already cover AES content.
3. **Preserve AES IDs** — keep `AES-NNNN` numbering for traceability.
4. **One package at a time** — complete validation report before starting the next package.

---

## Related Documents

- [README.md](README.md) — spec reading order
- [PLATFORM-COMPLETE.md](PLATFORM-COMPLETE.md) — platform sign-off

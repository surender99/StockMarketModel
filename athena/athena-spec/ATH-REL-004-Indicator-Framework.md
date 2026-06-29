# ATH-REL-004 – Indicator Framework (Release-04)

> **Version:** v0.1  
> **Source:** `References/ATH-REL-004-Indicator-Framework.zip`  
> **Status:** Spec-integrated (skeleton release package)  
> **Validation:** [packages/PACKAGE-REL-004-COMPLETE.md](packages/PACKAGE-REL-004-COMPLETE.md)

ATH-REL-004 is the **indicator framework release package** for Athena Release-04. It extends REL-003 feature engineering with a full indicator catalog, execution engine, composition, and output validation.

---

## Purpose

| Aspect | Detail |
|--------|--------|
| **What** | Indicator engine, expanded catalog (WMA, ROC, OBV, CMF, MFI, CCI, Williams %R), validation, composition |
| **When** | After REL-003 feature registry and pipeline are wired |
| **Who** | `athena-core` developers, strategy authors, AI coding agents |

Release-04 v0.1 ships as a **skeleton**: section READMEs are placeholders. Canonical content lives in ATH/AES documents, REQ files, and `athena-core` modules cross-linked from [release-04/](release-04/README.md).

---

## Relationship to Prior Releases

| ID | Role | Canonical Path |
|----|------|----------------|
| **ATH-REL-003** | Feature registry, pipeline, cache | [ATH-REL-003-Feature-Engineering.md](ATH-REL-003-Feature-Engineering.md) |
| **Package 05** | Feature engineering AES specs | [feature-engineering/](feature-engineering/) |
| **AES-0501** | Indicator framework | [AES-0501](feature-engineering/framework/AES-0501-Indicator-Framework.md) |

**Reading order:** ATH-REL-003 → ATH-REL-004 (this index) → AES-0501 → REQ-IND-*.

**Implementation order (from zip Overview):** architecture → engine → registry → moving averages → trend → momentum → volume → volatility → oscillators → breadth → composition → validation → testing.

---

## Release Package Sections (v0.1)

| # | Section | Zip Folder | Canonical Spec / Code |
|---|---------|------------|------------------------|
| 00 | Executive Summary | `00-Executive-Summary` | This document |
| 01 | Indicator Architecture | `01-Indicator-Architecture` | [AES-0501](feature-engineering/framework/AES-0501-Indicator-Framework.md) |
| 02 | Indicator Engine | `02-Indicator-Engine` | `domain/indicators/engine.py`, REQ-IND-ENGINE-001 |
| 03 | Indicator Registry | `03-Indicator-Registry` | `domain/features/indicator_plugins.py` |
| 04 | Moving Averages | `04-Moving-Averages` | `domain/indicators/wma.py`, REQ-IND-WMA-001 |
| 05 | Trend Indicators | `05-Trend-Indicators` | `domain/indicators/adx.py` (REL-003) |
| 06 | Momentum Indicators | `06-Momentum-Indicators` | `domain/indicators/roc.py`, REQ-IND-ROC-001 |
| 07 | Volume Indicators | `07-Volume-Indicators` | `domain/indicators/obv.py`, `cmf.py`, `mfi.py` |
| 08 | Volatility Indicators | `08-Volatility-Indicators` | `domain/indicators/atr.py`, `bollinger.py` (REL-003) |
| 09 | Oscillators | `09-Oscillators` | `domain/indicators/cci.py`, `willr.py` |
| 10 | Market Breadth | `10-Market-Breadth` | `application/breadth_engine.py` (Package 04) |
| 11 | Indicator Composition | `11-Indicator-Composition` | `IndicatorEngine.compute_many` |
| 12 | Indicator Validation | `12-Indicator-Validation` | `domain/indicators/validation.py` |
| 13 | Testing | `13-Testing` | `tests/test_indicator_framework.py` |
| 14 | Benchmarks | `14-Benchmarks` | [athena-core/benchmarks/](../athena-core/benchmarks/README.md) |
| 15 | AI Coding | `15-AI-Coding` | [AES-0006](governance/AES-0006-AI-Coding-Standards.md) |
| 16 | Agent Packages | `16-Agent-Packages` | [prompts/](prompts/) |
| 17 | Playbooks | `17-Implementation-Playbooks` | [athena-docs/handbook/](../athena-docs/handbook/) |

Full section index: [release-04/README.md](release-04/README.md).

---

## Implemented vs Documented-Only (v0.1)

| Category | Status | Evidence |
|----------|--------|----------|
| IndicatorEngine | ✅ Implemented | `domain/indicators/engine.py` |
| Output validation | ✅ Implemented | `domain/indicators/validation.py` |
| WMA, ROC, OBV, CMF, MFI, CCI, Williams %R | ✅ Implemented | New `domain/indicators/*.py` |
| Multi-indicator composition | ✅ Implemented | `IndicatorEngine.compute_many` |
| SuperTrend, Keltner, VWAP, DMI | 📋 Documented-only | Deferred to future releases |
| Section placeholder READMEs in zip | 📋 Skeleton only | Mapped to canonical paths above |

---

## Related Documents

- [ATH-REL-003 Feature Engineering](ATH-REL-003-Feature-Engineering.md)
- [indicator-catalog.md](feature-engineering/indicators/indicator-catalog.md)
- [REFERENCES-INDEX](REFERENCES-INDEX.md)
- [contracts/IndicatorProvider.md](contracts/IndicatorProvider.md)

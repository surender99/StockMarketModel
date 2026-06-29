# ATH-REL-002 – Data Platform (Release-02)

> **Version:** v0.1  
> **Source:** `References/ATH-REL-002-Data-Platform.zip`  
> **Status:** Spec-integrated (skeleton release package)  
> **Validation:** [packages/PACKAGE-REL-002-COMPLETE.md](packages/PACKAGE-REL-002-COMPLETE.md)

ATH-REL-002 is the **data platform release package** for Athena Release-02. It defines the taxonomy and implementation order for historical data, validation, cleaning, versioning, instrument master, dataset registry, and feature-store integration used by indicators, backtesting, and research modules.

---

## Purpose

| Aspect | Detail |
|--------|--------|
| **What** | Data platform: OHLCV ingest/storage, NSE calendar, quality gates, cleaning, versioning, instrument master, dataset registry |
| **When** | Applied after ATH-REL-001 core framework and before feature/backtest extensions |
| **Who** | `athena-core` developers, SDK/CLI integrators, AI coding agents |

Release-02 v0.1 ships as a **skeleton**: section READMEs are placeholders. Canonical, actionable content lives in existing ATH/AES documents and `athena-core` modules cross-linked from [release-02/](release-02/README.md).

---

## Relationship to Prior Releases and athena-core

| ID | Role | Canonical Path |
|----|------|----------------|
| **ATH-REL-000** | Release-00 engineering standards taxonomy | [ATH-REL-000-Engineering-Standards.md](ATH-REL-000-Engineering-Standards.md) |
| **ATH-REL-001** | Release-01 core framework taxonomy | [ATH-REL-001-Core-Framework.md](ATH-REL-001-Core-Framework.md) |
| **ATH-REL-002** | Release-02 data platform taxonomy | This document |
| **ATH-003** | Repository layout and Clean Architecture | [ATH-003-Repository-Architecture.md](ATH-003-Repository-Architecture.md) |
| **AES-0300** | Data platform scope | [data/AES-0300-Data-Platform.md](data/AES-0300-Data-Platform.md) |
| **Package 03** | DataProvider contract and quality | [contracts/DataProvider.md](contracts/DataProvider.md) |

**Reading order:** ATH-REL-001 (core) → ATH-REL-002 (this index) → ATH-003 (repo) → AES-0300/0310 (data) → REQ-DATA-*.

**Implementation order (from zip Overview):** Historical Data → Live Market Data → Instrument Master → Corporate Actions → Trading Calendar → Data Validation → Data Cleaning → Data Versioning → Feature Store → Dataset Registry → Testing → Benchmarks.

---

## Release Package Sections (v0.1)

| # | Section | Zip Folder | Canonical Spec / Code |
|---|---------|------------|------------------------|
| 00 | Executive Summary | `00-Executive-Summary` | This document |
| 01 | Historical Data | `01-Historical-Data` | `ingest_ohlcv.py`, `yfinance_client.py`, `parquet_ohlcv_store.py` |
| 02 | Live Market Data | `02-Live-Market-Data` | 📋 Deferred — streaming adapters |
| 03 | Instrument Master | `03-Instrument-Master` | `infrastructure/instrument_master.py`, `config/instruments.yaml` |
| 04 | Corporate Actions | `04-Corporate-Actions` | 📋 Deferred — `auto_adjust` policy in ADR-0002 |
| 05 | Trading Calendar | `05-Trading-Calendar` | `nse_calendar.py`, `REQ-DATA-CALENDAR-001` |
| 06 | Data Validation | `06-Data-Validation` | `domain/data/quality.py`, `REQ-DATA-QUALITY-001` |
| 07 | Data Cleaning | `07-Data-Cleaning` | `domain/data/cleaning.py` |
| 08 | Data Versioning | `08-Data-Versioning` | `domain/data/versioning.py`, Parquet metadata sidecar |
| 09 | Feature Store | `09-Feature-Store` | `parquet_feature_store.py`, `REQ-FEAT-STORE-001` |
| 10 | Dataset Registry | `10-Dataset-Registry` | `file_dataset_registry.py`, `domain/data/registry.py` |
| 11 | Testing | `11-Testing` | `tests/test_data_platform.py`, `tests/test_data_quality.py` |
| 12 | Benchmarks | `12-Benchmarks` | [athena-core/benchmarks/](../athena-core/benchmarks/README.md) |
| 13 | AI Coding | `13-AI-Coding` | [AES-0006](governance/AES-0006-AI-Coding-Standards.md) |
| 14 | Agent Packages | `14-Agent-Packages` | 📋 Skeleton only |
| 15 | Playbooks | `15-Implementation-Playbooks` | [athena-docs/handbook/](../athena-docs/handbook/) |

Full section index: [release-02/README.md](release-02/README.md).

---

## Implemented vs Documented-Only (v0.1)

| Category | Status | Evidence |
|----------|--------|----------|
| OHLCV ingest (yfinance → Parquet) | ✅ Implemented | `IngestOHLCVUseCase`, `REQ-DATA-INGEST-001` |
| NSE trading calendar | ✅ Implemented | `NSETradingCalendar`, `REQ-DATA-CALENDAR-001` |
| Data quality checks | ✅ Implemented | `check_ohlcv_quality`, `REQ-DATA-QUALITY-001` |
| Data cleaning pipeline | ✅ Implemented | `clean_ohlcv_frame`, ingest integration |
| Data versioning & immutability | ✅ Implemented | metadata sidecar, `DataPlatformConfig.versioning` |
| Instrument master (YAML) | ✅ Implemented | `YamlInstrumentMaster`, `config/instruments.yaml` |
| Dataset registry | ✅ Implemented | `FileDatasetRegistry`, ingest auto-register |
| Data platform bootstrap | ✅ Implemented | `DataContext`, `bootstrap_data_platform` |
| Feature store (Parquet) | ✅ Implemented | `ParquetFeatureStore`, `REQ-FEAT-STORE-001` |
| Live streaming feeds | 📋 Documented-only | Deferred |
| Corporate actions adjustment | 📋 Documented-only | MVP uses `auto_adjust=False` per ADR-0002 |
| Section placeholder READMEs in zip | 📋 Skeleton only | Mapped to canonical paths above |
| `ATH-REL-002-Overview.docx` | 📋 Binary only | Section list captured in this document |

---

## REQ Traceability (Release-02)

| REQ ID | Section | Module |
|--------|---------|--------|
| REQ-DATA-INGEST-001 | 01 Historical Data | `application/ingest_ohlcv.py`, `infrastructure/yfinance_client.py` |
| REQ-DATA-CALENDAR-001 | 05 Trading Calendar | `infrastructure/nse_calendar.py` |
| REQ-DATA-QUALITY-001 | 06 Data Validation | `domain/data/quality.py` |
| REQ-DATA-CLEAN-001 | 07 Data Cleaning | `domain/data/cleaning.py` |
| REQ-DATA-VERSION-001 | 08 Data Versioning | `domain/data/versioning.py`, `parquet_ohlcv_store.py` |
| REQ-DATA-INSTR-001 | 03 Instrument Master | `infrastructure/instrument_master.py` |
| REQ-DATA-REGISTRY-001 | 10 Dataset Registry | `infrastructure/file_dataset_registry.py` |
| REQ-FEAT-STORE-001 | 09 Feature Store | `infrastructure/parquet_feature_store.py` |

---

## Related Documents

- [ATH-REL-001 Core Framework](ATH-REL-001-Core-Framework.md)
- [ATH-003 Repository Architecture](ATH-003-Repository-Architecture.md)
- [REFERENCES-INDEX](REFERENCES-INDEX.md)
- [DataProvider Contract](contracts/DataProvider.md)
- [PACKAGE-03-COMPLETE](packages/PACKAGE-03-COMPLETE.md)

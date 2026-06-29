# ATH-REL-002 Data Platform — Section Index

> **Release package:** [ATH-REL-002-Data-Platform.md](../ATH-REL-002-Data-Platform.md)  
> **Source zip:** `References/ATH-REL-002-Data-Platform.zip`

This index maps the ATH-REL-002 Release-02 folder taxonomy to canonical specs and `athena-core` modules. Do not duplicate content here — follow the links.

---

## Section Map

| Section | Zip Status (v0.1) | Canonical Spec | Code / Tooling |
|---------|-------------------|----------------|----------------|
| **00 Executive Summary** | Placeholder | [ATH-REL-002](../ATH-REL-002-Data-Platform.md) | — |
| **01 Historical Data** | Placeholder | [REQ-DATA-INGEST-001](../requirements/REQ-DATA-INGEST-001.md) | `application/ingest_ohlcv.py`, `infrastructure/yfinance_client.py`, `parquet_ohlcv_store.py` |
| **02 Live Market Data** | Placeholder | [AES-0300](../data/AES-0300-Data-Platform.md) | 📋 Deferred |
| **03 Instrument Master** | Placeholder | [ATH-REL-002](../ATH-REL-002-Data-Platform.md) | `infrastructure/instrument_master.py`, `config/instruments.yaml` |
| **04 Corporate Actions** | Placeholder | [ADR-0002](../adrs/ADR-0002-yfinance-mvp-data-source.md) | 📋 Deferred |
| **05 Trading Calendar** | Placeholder | [REQ-DATA-CALENDAR-001](../requirements/REQ-DATA-CALENDAR-001.md) | `infrastructure/nse_calendar.py` |
| **06 Data Validation** | Placeholder | [REQ-DATA-QUALITY-001](../requirements/REQ-DATA-QUALITY-001.md) | `domain/data/quality.py` |
| **07 Data Cleaning** | Placeholder | [ATH-REL-002](../ATH-REL-002-Data-Platform.md) | `domain/data/cleaning.py` |
| **08 Data Versioning** | Placeholder | [ATH-REL-002](../ATH-REL-002-Data-Platform.md) | `domain/data/versioning.py`, Parquet metadata |
| **09 Feature Store** | Placeholder | [REQ-FEAT-STORE-001](../requirements/REQ-FEAT-STORE-001.md) | `infrastructure/parquet_feature_store.py` |
| **10 Dataset Registry** | Placeholder | [ATH-REL-002](../ATH-REL-002-Data-Platform.md) | `infrastructure/file_dataset_registry.py` |
| **11 Testing** | Placeholder | [ATH-002](../ATH-002-Engineering-Standards.md) | `tests/test_data_platform.py` |
| **12 Benchmarks** | Placeholder | [athena-core/benchmarks/](../../athena-core/benchmarks/README.md) | `tests/benchmarks/` |
| **13 AI Coding** | Placeholder | [AES-0006](../governance/AES-0006-AI-Coding-Standards.md) | — |
| **14 Agent Packages** | Placeholder | — | 📋 Skeleton only |
| **15 Playbooks** | Placeholder | [athena-docs/handbook/](../../athena-docs/handbook/) | — |

---

## REQ Traceability (Release-02)

| REQ ID | Section | Module |
|--------|---------|--------|
| REQ-DATA-INGEST-001 | 01 Historical Data | `application/ingest_ohlcv.py` |
| REQ-DATA-CALENDAR-001 | 05 Trading Calendar | `infrastructure/nse_calendar.py` |
| REQ-DATA-QUALITY-001 | 06 Data Validation | `domain/data/quality.py` |
| REQ-DATA-CLEAN-001 | 07 Data Cleaning | `domain/data/cleaning.py` |
| REQ-DATA-VERSION-001 | 08 Data Versioning | `domain/data/versioning.py` |
| REQ-DATA-INSTR-001 | 03 Instrument Master | `infrastructure/instrument_master.py` |
| REQ-DATA-REGISTRY-001 | 10 Dataset Registry | `infrastructure/file_dataset_registry.py` |
| REQ-FEAT-STORE-001 | 09 Feature Store | `infrastructure/parquet_feature_store.py` |

---

## Bootstrap Wiring

`bootstrap_data_platform(config)` returns `DataContext` with calendar, OHLCV repository, dataset registry, and instrument master. `AthenaRuntime.data` exposes this context; `bootstrap_athena_core` registers it in the DI container as `"data"`.

# ATH-REL-003 Feature Engineering — Section Index

> **Release package:** [ATH-REL-003-Feature-Engineering.md](../ATH-REL-003-Feature-Engineering.md)  
> **Source zip:** `References/ATH-REL-003-Feature-Engineering.zip`

This index maps the ATH-REL-003 Release-03 folder taxonomy to canonical specs and `athena-core` modules. Do not duplicate content here — follow the links.

---

## Section Map

| Section | Zip Status (v0.1) | Canonical Spec | Code / Tooling |
|---------|-------------------|----------------|----------------|
| **00 Executive Summary** | Placeholder | [ATH-REL-003](../ATH-REL-003-Feature-Engineering.md) | — |
| **01 OHLC Features** | Placeholder | [REQ-IND-EMA-001](../requirements/REQ-IND-EMA-001.md) | `domain/indicators/ema.py`, `sma.py` |
| **02 Returns Features** | Placeholder | — | Deferred |
| **03 Volume Features** | Placeholder | [indicator-catalog](../feature-engineering/indicators/indicator-catalog.md) | Deferred |
| **04 Volatility Features** | Placeholder | [REQ-IND-ATR-001](../requirements/REQ-IND-ATR-001.md), [REQ-IND-BOLLINGER-001](../requirements/REQ-IND-BOLLINGER-001.md) | `domain/indicators/atr.py`, `bollinger.py` |
| **05 Trend Features** | Placeholder | [REQ-IND-ADX-001](../requirements/REQ-IND-ADX-001.md) | `domain/indicators/adx.py` |
| **06 Momentum Features** | Placeholder | [REQ-IND-RSI-001](../requirements/REQ-IND-RSI-001.md), [REQ-IND-MACD-001](../requirements/REQ-IND-MACD-001.md) | `domain/indicators/rsi.py`, `macd.py`, `stoch.py` |
| **07 Time/Session** | Placeholder | — | Deferred |
| **08 Cross-Asset** | Placeholder | — | Deferred |
| **09 Feature Registry** | Placeholder | [REQ-FEAT-REGISTRY-001](../requirements/REQ-FEAT-REGISTRY-001.md) | `domain/features/indicator_plugins.py` |
| **10 Feature Pipeline** | Placeholder | [REQ-FEAT-PIPELINE-001](../requirements/REQ-FEAT-PIPELINE-001.md) | `application/feature_pipeline.py` |
| **11 Feature Validation** | Placeholder | [REQ-FEAT-CACHE-001](../requirements/REQ-FEAT-CACHE-001.md) | `domain/features/caching.py`, `feature_service.py` |
| **12 Testing** | Placeholder | [ATH-002](../ATH-002-Engineering-Standards.md) | `tests/test_feature_engineering_framework.py` |
| **13 Benchmarks** | Placeholder | [athena-core/benchmarks/](../../athena-core/benchmarks/README.md) | `tests/benchmarks/` |
| **14 AI Coding** | Placeholder | [AES-0006](../governance/AES-0006-AI-Coding-Standards.md) | — |
| **15 Agent Packages** | Placeholder | [prompts/](../prompts/) | — |
| **16 Playbooks** | Placeholder | [athena-docs/handbook/](../../athena-docs/handbook/) | — |

---

## REQ Traceability (Release-03)

| REQ ID | Section | Module |
|--------|---------|--------|
| REQ-FEAT-REGISTRY-001 | 09 Feature Registry | `domain/features/indicator_plugins.py` |
| REQ-FEAT-PIPELINE-001 | 10 Feature Pipeline | `application/feature_pipeline.py` |
| REQ-FEAT-CACHE-001 | 11 Feature Validation | `domain/features/caching.py` |
| REQ-FEAT-STORE-001 | 11 Feature Validation | `application/feature_service.py`, `infrastructure/parquet_feature_store.py` |
| REQ-IND-ATR-001 | 04 Volatility | `domain/indicators/atr.py` |
| REQ-IND-ADX-001 | 05 Trend | `domain/indicators/adx.py` |
| REQ-IND-BOLLINGER-001 | 04 Volatility | `domain/indicators/bollinger.py` |
| REQ-IND-EMA-001 | 01 OHLC / 05 Trend | `domain/indicators/ema.py` |
| REQ-IND-SMA-001 | 01 OHLC / 05 Trend | `domain/indicators/sma.py` |
| REQ-IND-MACD-001 | 06 Momentum | `domain/indicators/macd.py` |
| REQ-IND-RSI-001 | 06 Momentum | `domain/indicators/rsi.py` |
| REQ-IND-STOCH-001 | 06 Momentum | `domain/indicators/stoch.py` |

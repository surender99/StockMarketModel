# ATH-REL-004 Indicator Framework — Section Index

> **Release package:** [ATH-REL-004-Indicator-Framework.md](../ATH-REL-004-Indicator-Framework.md)  
> **Source zip:** `References/ATH-REL-004-Indicator-Framework.zip`

This index maps the ATH-REL-004 Release-04 folder taxonomy to canonical specs and `athena-core` modules.

---

## Section Map

| Section | Zip Status (v0.1) | Canonical Spec | Code / Tooling |
|---------|-------------------|----------------|----------------|
| **00 Executive Summary** | Placeholder | [ATH-REL-004](../ATH-REL-004-Indicator-Framework.md) | — |
| **01 Indicator Architecture** | Placeholder | [AES-0501](../feature-engineering/framework/AES-0501-Indicator-Framework.md) | — |
| **02 Indicator Engine** | Placeholder | [REQ-IND-ENGINE-001](../requirements/REQ-IND-ENGINE-001.md) | `domain/indicators/engine.py` |
| **03 Indicator Registry** | Placeholder | [REQ-FEAT-REGISTRY-001](../requirements/REQ-FEAT-REGISTRY-001.md) | `domain/features/indicator_plugins.py` |
| **04 Moving Averages** | Placeholder | [REQ-IND-WMA-001](../requirements/REQ-IND-WMA-001.md) | `domain/indicators/wma.py` |
| **05 Trend Indicators** | Placeholder | [REQ-IND-ADX-001](../requirements/REQ-IND-ADX-001.md) | `domain/indicators/adx.py` |
| **06 Momentum Indicators** | Placeholder | [REQ-IND-ROC-001](../requirements/REQ-IND-ROC-001.md) | `domain/indicators/roc.py` |
| **07 Volume Indicators** | Placeholder | [REQ-IND-OBV-001](../requirements/REQ-IND-OBV-001.md), [REQ-IND-CMF-001](../requirements/REQ-IND-CMF-001.md), [REQ-IND-MFI-001](../requirements/REQ-IND-MFI-001.md) | `domain/indicators/obv.py`, `cmf.py`, `mfi.py` |
| **08 Volatility Indicators** | Placeholder | [REQ-IND-ATR-001](../requirements/REQ-IND-ATR-001.md) | `domain/indicators/atr.py`, `bollinger.py` |
| **09 Oscillators** | Placeholder | [REQ-IND-CCI-001](../requirements/REQ-IND-CCI-001.md), [REQ-IND-WILLR-001](../requirements/REQ-IND-WILLR-001.md) | `domain/indicators/cci.py`, `willr.py` |
| **10 Market Breadth** | Placeholder | [REQ-MI-001](../requirements/REQ-MI-001.md) | `application/breadth_engine.py` |
| **11 Indicator Composition** | Placeholder | [REQ-IND-COMPOSITION-001](../requirements/REQ-IND-COMPOSITION-001.md) | `IndicatorEngine.compute_many` |
| **12 Indicator Validation** | Placeholder | [REQ-IND-VALIDATION-001](../requirements/REQ-IND-VALIDATION-001.md) | `domain/indicators/validation.py` |
| **13 Testing** | Placeholder | [ATH-002](../ATH-002-Engineering-Standards.md) | `tests/test_indicator_framework.py` |
| **14 Benchmarks** | Placeholder | [athena-core/benchmarks/](../../athena-core/benchmarks/README.md) | `tests/benchmarks/` |
| **15 AI Coding** | Placeholder | [AES-0006](../governance/AES-0006-AI-Coding-Standards.md) | — |
| **16 Agent Packages** | Placeholder | [prompts/](../prompts/) | — |
| **17 Playbooks** | Placeholder | [athena-docs/handbook/](../../athena-docs/handbook/) | — |

---

## REQ Traceability (Release-04)

| REQ ID | Section | Module |
|--------|---------|--------|
| REQ-IND-ENGINE-001 | 02 Indicator Engine | `domain/indicators/engine.py` |
| REQ-IND-VALIDATION-001 | 12 Indicator Validation | `domain/indicators/validation.py` |
| REQ-IND-COMPOSITION-001 | 11 Indicator Composition | `domain/indicators/engine.py` |
| REQ-IND-WMA-001 | 04 Moving Averages | `domain/indicators/wma.py` |
| REQ-IND-ROC-001 | 06 Momentum | `domain/indicators/roc.py` |
| REQ-IND-OBV-001 | 07 Volume | `domain/indicators/obv.py` |
| REQ-IND-CMF-001 | 07 Volume | `domain/indicators/cmf.py` |
| REQ-IND-MFI-001 | 07 Volume | `domain/indicators/mfi.py` |
| REQ-IND-CCI-001 | 09 Oscillators | `domain/indicators/cci.py` |
| REQ-IND-WILLR-001 | 09 Oscillators | `domain/indicators/willr.py` |

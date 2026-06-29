# ATH-REL-006 Strategy Engine — Section Index

> **Release package:** [ATH-REL-006-Strategy-Engine.md](../ATH-REL-006-Strategy-Engine.md)  
> **Source doc:** `References/REL-006-Strategy Engine.docx`

This index maps the ATH-REL-006 Release-06 module taxonomy to canonical specs and `athena-core` modules.

---

## Section Map

| Section | Doc Status (v0.1) | Canonical Spec | Code / Tooling |
|---------|-------------------|----------------|----------------|
| **00 Executive Summary** | From docx §1 | [ATH-REL-006](../ATH-REL-006-Strategy-Engine.md) | — |
| **01 Strategy Framework** | From docx §5.1 | [AES-0700](../strategy-engine/framework/AES-0700-Strategy-Engine.md) | `domain/strategy/engine.py` |
| **02 Strategy Registry** | From docx §5.2 | [REQ-STRAT-REGISTRY-001](../requirements/REQ-STRAT-REGISTRY-001.md) | `domain/strategy/strategy_plugins.py` |
| **03 Signal Engine** | From docx §5.3 | [REQ-STRAT-CONFIG-001](../requirements/REQ-STRAT-CONFIG-001.md) | `domain/strategy/signals.py`, `types.py` |
| **04 Entry Rules** | From docx §5.4 | [REQ-STRAT-CONFIG-001](../requirements/REQ-STRAT-CONFIG-001.md) | `domain/strategy/builtin.py` |
| **05 Exit Rules** | From docx §5.5 | [REQ-STRAT-CONFIG-001](../requirements/REQ-STRAT-CONFIG-001.md) | `domain/strategy/signals.py` |
| **06 Risk Management** | From docx §5.6 | — | `domain/strategy/risk.py` |
| **07 Position Sizing** | From docx §5.7 | — | `domain/strategy/position_sizing.py` |
| **08 Multi-Timeframe** | From docx §5.8 | — | Deferred |
| **09 Strategy Composition** | From docx §5.9 | — | `domain/strategy/composition.py` |
| **10 Strategy Validation** | From docx §5.10 | — | `domain/strategy/validation.py` |
| **11 Testing** | From docx §9 | [ATH-002](../ATH-002-Engineering-Standards.md) | `tests/test_strategy_engine_framework.py` |
| **12 Benchmarks** | From docx §10 | [athena-core/benchmarks/](../../athena-core/benchmarks/README.md) | `tests/benchmarks/` |
| **13 AI Coding** | From docx §11 | [AES-0006](../governance/AES-0006-AI-Coding-Standards.md) | — |
| **14 Agent Packages** | From docx §8 | [prompts/](../prompts/) | — |
| **15 Playbooks** | — | [athena-docs/handbook/](../../athena-docs/handbook/) | — |

---

## REQ Traceability (Release-06)

| REQ ID | Section | Module |
|--------|---------|--------|
| REQ-STRAT-REGISTRY-001 | 02 Strategy Registry | `domain/strategy/strategy_plugins.py` |
| REQ-STRAT-CONFIG-001 | 01/04/05 Rules | `domain/strategy/config.py`, `builtin.py` |
| FR-009 | 03 Signal Engine | `domain/strategy/types.py` |
| FR-012 | 09 Composition | `domain/strategy/composition.py` |

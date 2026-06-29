# ATH-REL-006 – Strategy Engine (Release-06)

> **Version:** v0.1  
> **Source:** `References/REL-006-Strategy Engine.docx`  
> **Status:** Spec-integrated (skeleton release package)  
> **Validation:** [packages/PACKAGE-REL-006-COMPLETE.md](packages/PACKAGE-REL-006-COMPLETE.md)

ATH-REL-006 is the **strategy engine release package** for Athena Release-06. It extends Package 07 strategy engine with StrategyProvider plugin registration, signal engine, composition, validation, position sizing, and risk modules.

---

## Purpose

| Aspect | Detail |
|--------|--------|
| **What** | Strategy registry, signal engine, entry/exit rules, risk, position sizing, composition, validation |
| **When** | After REL-004 indicators and REL-005 patterns |
| **Who** | `athena-core` developers, strategy authors, AI coding agents |

Release-06 v0.1 ships as a **skeleton**: the Word document defines module taxonomy; canonical content lives in ATH/AES documents, REQ files, and `athena-core` modules cross-linked from [release-06/](release-06/README.md).

---

## Relationship to Prior Releases

| ID | Role | Canonical Path |
|----|------|----------------|
| **ATH-REL-003** | Feature pipeline | [ATH-REL-003-Feature-Engineering.md](ATH-REL-003-Feature-Engineering.md) |
| **ATH-REL-004** | Indicator engine | [ATH-REL-004-Indicator-Framework.md](ATH-REL-004-Indicator-Framework.md) |
| **ATH-REL-005** | Pattern recognition | [ATH-REL-005-Pattern-Recognition.md](ATH-REL-005-Pattern-Recognition.md) |
| **Package 07** | Strategy engine AES specs | [strategy-engine/](strategy-engine/) |
| **AES-0700** | Strategy engine framework | [AES-0700](strategy-engine/framework/AES-0700-Strategy-Engine.md) |

**Reading order:** ATH-REL-003 → REL-004 → REL-005 → ATH-REL-006 (this index) → REQ-STRAT-*.

---

## Release Package Sections (v0.1)

| # | Section | Doc Module | Canonical Spec / Code |
|---|---------|------------|------------------------|
| 00 | Executive Summary | §1 | This document |
| 01 | Strategy Framework | §5.1 | `domain/strategy/engine.py`, `config.py` |
| 02 | Strategy Registry | §5.2 | `domain/strategy/strategy_plugins.py`, REQ-STRAT-REGISTRY-001 |
| 03 | Signal Engine | §5.3 | `domain/strategy/signals.py`, `types.py` |
| 04 | Entry Rules | §5.4 | `domain/strategy/builtin.py`, REQ-STRAT-CONFIG-001 |
| 05 | Exit Rules | §5.5 | `domain/strategy/signals.py` |
| 06 | Risk Management | §5.6 | `domain/strategy/risk.py` |
| 07 | Position Sizing | §5.7 | `domain/strategy/position_sizing.py` |
| 08 | Multi-Timeframe Engine | §5.8 | Deferred |
| 09 | Strategy Composition | §5.9 | `domain/strategy/composition.py` |
| 10 | Strategy Validation | §5.10 | `domain/strategy/validation.py` |
| 11 | Testing | §9 | `tests/test_strategy_engine_framework.py` |
| 12 | Benchmarks | §10 | [athena-core/benchmarks/](../athena-core/benchmarks/README.md) |
| 13 | AI Coding | §11 | [AES-0006](governance/AES-0006-AI-Coding-Standards.md) |
| 14 | Agent Packages | §8 | [prompts/](prompts/) |
| 15 | Playbooks | — | [athena-docs/handbook/](../athena-docs/handbook/) |

Full section index: [release-06/README.md](release-06/README.md).

---

## Functional Requirements (FR-001–FR-015)

| ID | Requirement | v0.1 Status |
|----|-------------|-------------|
| FR-001 | Multiple strategies simultaneously | ✅ PluginRegistry |
| FR-002 | Dynamic loading | ✅ `resolve_strategy` |
| FR-003 | Strategy registration | ✅ `register_builtin_strategies` |
| FR-004 | Reusable entry rules | ✅ `RuleSpec` + builtins |
| FR-005 | Reusable exit rules | ✅ `ExitRuleSpec` |
| FR-006 | Reusable filters | ✅ Existing `FilterSpec` |
| FR-007 | Reusable risk modules | ✅ `risk.py` |
| FR-008 | Reusable position sizing | ✅ `position_sizing.py` |
| FR-009 | Signal confidence | ✅ `TradeSignal.confidence` |
| FR-010 | Parameter injection | ✅ `StrategyConfig` Pydantic |
| FR-011 | Configuration files | ✅ YAML loader (REQ-STRAT-CONFIG-001) |
| FR-012 | Strategy composition | ✅ `composition.py` |
| FR-013 | Multiple symbols | ✅ `UniverseConfig` |
| FR-014 | Multiple exchanges | 📋 Deferred |
| FR-015 | Multiple timeframes | 📋 Deferred (§5.8) |

---

## Implemented vs Documented-Only (v0.1)

| Category | Status | Evidence |
|----------|--------|----------|
| StrategyProvider plugin registry | ✅ Implemented | `register_builtin_strategies`, `resolve_strategy` |
| Bootstrap wiring | ✅ Implemented | `application/bootstrap.py` |
| Signal engine | ✅ Implemented | `domain/strategy/signals.py` |
| Builtin strategies (EMA crossover, pullback) | ✅ Implemented | `domain/strategy/builtin.py` |
| Composition (AND/OR/NOT/weighted/voting) | ✅ Implemented | `domain/strategy/composition.py` |
| Validation | ✅ Implemented | `domain/strategy/validation.py` |
| Position sizing extensions | ✅ Implemented | pct_risk, atr_based, fixed_quantity |
| Multi-timeframe engine | 📋 Documented-only | Deferred |
| DSL, optimizer agent packages | 📋 Documented-only | Deferred |

---

## Related Documents

- [ATH-REL-005 Pattern Recognition](ATH-REL-005-Pattern-Recognition.md)
- [contracts/StrategyProvider.md](contracts/StrategyProvider.md)
- [REQ-STRAT-CONFIG-001](requirements/REQ-STRAT-CONFIG-001.md)
- [REFERENCES-INDEX](REFERENCES-INDEX.md)

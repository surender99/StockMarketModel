# ATH-REL-007 – Backtesting Engine (Release-07)

> **Version:** v0.1  
> **Source:** `References/REL-007-Backtesting Engine.docx`  
> **Status:** Spec-integrated (skeleton release package)  
> **Validation:** [packages/PACKAGE-REL-007-COMPLETE.md](packages/PACKAGE-REL-007-COMPLETE.md)

ATH-REL-007 is the **backtesting engine release package** for Athena Release-07. It extends Package 08 backtesting with order engine, execution models, slippage models, trade journal, advanced metrics, and BacktestManager orchestration.

---

## Purpose

| Aspect | Detail |
|--------|--------|
| **What** | Order simulation, execution models, portfolio simulation, performance analytics, walk-forward integration |
| **When** | After REL-006 strategy engine |
| **Who** | `athena-core` developers, quant researchers, AI coding agents |

Release-07 v0.1 ships as a **skeleton**: the Word document defines module taxonomy; canonical content lives in ATH/AES documents, REQ files, and `athena-core` modules cross-linked from [release-07/](release-07/README.md).

---

## Relationship to Prior Releases

| ID | Role | Canonical Path |
|----|------|----------------|
| **ATH-REL-006** | Strategy engine | [ATH-REL-006-Strategy-Engine.md](ATH-REL-006-Strategy-Engine.md) |
| **Package 08** | Backtesting AES specs | [backtesting/](backtesting/) |
| **AES-0800** | Backtesting engine framework | [AES-0800](backtesting/framework/AES-0800-Backtesting-Engine.md) |
| **AES-0801** | Execution model | [AES-0801](backtesting/framework/AES-0801-Execution-Model.md) |

**Reading order:** ATH-REL-006 → Package 08 → ATH-REL-007 (this index) → REQ-BT-*.

---

## Release Package Sections (v0.1)

| # | Section | Doc Module | Canonical Spec / Code |
|---|---------|------------|------------------------|
| 00 | Executive Summary | §1 | This document |
| 01 | Backtest Engine | §5.1 | `application/backtest_manager.py`, `backtest_engine.py` |
| 02 | Order Engine | §5.2 | `domain/backtest/orders.py`, REQ-BT-ORDER-001 |
| 03 | Execution Engine | §5.3 | `domain/backtest/execution.py`, REQ-BT-EXECUTION-001 |
| 04 | Portfolio Simulator | §5.4 | `domain/portfolio/`, `portfolio_engine.py` |
| 05 | Position Manager | §5.5 | `domain/portfolio/positions.py` |
| 06 | Risk Engine | §5.6 | `portfolio_risk.py`, strategy `risk.py` |
| 07 | Brokerage Engine | §5.7 | `application/costs.py` |
| 08 | Slippage Engine | §5.8 | `domain/backtest/slippage.py` |
| 09 | Tax Engine | §5.9 | `application/costs.py` (STT, GST) |
| 10 | Corporate Actions | §5.10 | Deferred |
| 11 | Performance Analytics | §5.11 | `backtest_metrics.py`, `statistics_engine.py` |
| 12 | Trade Journal | §5.12 | `domain/backtest/trade_journal.py` |
| 13 | Walk-Forward Engine | §5.13 | `application/walk_forward.py`, REQ-WALK-FORWARD-001 |
| 14 | Monte Carlo Engine | §5.14 | `statistics_engine.py` (bootstrap/MC) |
| 15 | Testing | §9 | `tests/test_backtest_engine_framework.py` |
| 16 | Benchmarks | §10 | [athena-core/benchmarks/](../athena-core/benchmarks/README.md) |
| 17 | AI Coding | §11 | [AES-0006](governance/AES-0006-AI-Coding-Standards.md) |
| 18 | Agent Packages | §8 | [prompts/](prompts/) |
| 19 | Playbooks | — | [athena-docs/handbook/](../athena-docs/handbook/) |

Full section index: [release-07/README.md](release-07/README.md).

---

## Functional Requirements (FR-001–FR-015)

| ID | Requirement | v0.1 Status |
|----|-------------|-------------|
| FR-001 | Deterministic backtests | ✅ BacktestManager, BacktestSession |
| FR-002 | Multiple execution models | ✅ current_bar_close, next_bar_open |
| FR-003 | Configurable commissions | ✅ BacktestCostsConfig |
| FR-004 | Configurable slippage | ✅ percentage, fixed, atr_based, volume_based |
| FR-005 | Taxes | ✅ STT, GST on brokerage |
| FR-006 | Portfolio simulation | ✅ PortfolioEngine integration |
| FR-007 | Cash management | ✅ PortfolioState |
| FR-008 | Corporate actions | 📋 Deferred |
| FR-009 | Multiple strategies | 📋 Deferred |
| FR-010 | Trade journals | ✅ build_trade_journal |
| FR-011 | Advanced metrics | ✅ sortino, calmar, ulcer, recovery_factor |
| FR-012 | Monte Carlo | ✅ StatisticsEngine (existing) |
| FR-013 | Walk-forward validation | ✅ WalkForwardValidator (existing) |
| FR-014 | Parameter optimization inputs | ✅ Optimizer (existing) |
| FR-015 | Export reports | 📋 Deferred |

---

## Implemented vs Documented-Only (v0.1)

| Category | Status | Evidence |
|----------|--------|----------|
| BacktestManager / BacktestSession | ✅ Implemented | `application/backtest_manager.py` |
| Order engine + state machine | ✅ Implemented | `domain/backtest/orders.py` |
| Execution models | ✅ Implemented | `domain/backtest/execution.py` |
| Slippage models | ✅ Implemented | `domain/backtest/slippage.py` |
| Trade journal | ✅ Implemented | `domain/backtest/trade_journal.py` |
| Advanced metrics | ✅ Implemented | `backtest_metrics.compute_advanced_metrics` |
| Plugin registration | ✅ Implemented | `backtest_plugins.py`, bootstrap |
| Corporate actions, intrabar, tick replay | 📋 Documented-only | Deferred |
| Multi-strategy portfolio backtest | 📋 Documented-only | Deferred |

---

## Related Documents

- [ATH-REL-006 Strategy Engine](ATH-REL-006-Strategy-Engine.md)
- [contracts/Backtester.md](backtesting/contracts/Backtester.md)
- [REQ-BT-ENGINE-001](requirements/REQ-BT-ENGINE-001.md)
- [REQ-BT-EXECUTION-001](requirements/REQ-BT-EXECUTION-001.md)
- [REQ-BT-ORDER-001](requirements/REQ-BT-ORDER-001.md)
- [REFERENCES-INDEX](REFERENCES-INDEX.md)

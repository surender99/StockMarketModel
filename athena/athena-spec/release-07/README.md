# ATH-REL-007 Backtesting Engine — Section Index

> **Release package:** [ATH-REL-007-Backtesting-Engine.md](../ATH-REL-007-Backtesting-Engine.md)  
> **Source doc:** `References/REL-007-Backtesting Engine.docx`

This index maps the ATH-REL-007 Release-07 module taxonomy to canonical specs and `athena-core` modules.

---

## Section Map

| Section | Doc Status (v0.1) | Canonical Spec | Code / Tooling |
|---------|-------------------|----------------|----------------|
| **00 Executive Summary** | From docx §1 | [ATH-REL-007](../ATH-REL-007-Backtesting-Engine.md) | — |
| **01 Backtest Engine** | From docx §5.1 | [REQ-BT-ENGINE-001](../requirements/REQ-BT-ENGINE-001.md) | `application/backtest_manager.py` |
| **02 Order Engine** | From docx §5.2 | [REQ-BT-ORDER-001](../requirements/REQ-BT-ORDER-001.md) | `domain/backtest/orders.py` |
| **03 Execution Engine** | From docx §5.3 | [REQ-BT-EXECUTION-001](../requirements/REQ-BT-EXECUTION-001.md) | `domain/backtest/execution.py` |
| **04 Portfolio Simulator** | From docx §5.4 | [AES-0900](../portfolio-engine/framework/AES-0900-Portfolio-Engine.md) | `application/portfolio_engine.py` |
| **05 Position Manager** | From docx §5.5 | — | `domain/portfolio/positions.py` |
| **06 Risk Engine** | From docx §5.6 | — | `application/portfolio_risk.py` |
| **07 Brokerage Engine** | From docx §5.7 | — | `application/costs.py` |
| **08 Slippage Engine** | From docx §5.8 | — | `domain/backtest/slippage.py` |
| **09 Tax Engine** | From docx §5.9 | — | `application/costs.py` |
| **10 Corporate Actions** | From docx §5.10 | — | Deferred |
| **11 Performance Analytics** | From docx §5.11 | [performance-metrics.md](../backtesting/metrics/performance-metrics.md) | `backtest_metrics.py` |
| **12 Trade Journal** | From docx §5.12 | — | `domain/backtest/trade_journal.py` |
| **13 Walk-Forward** | From docx §5.13 | [REQ-WALK-FORWARD-001](../requirements/REQ-WALK-FORWARD-001.md) | `application/walk_forward.py` |
| **14 Monte Carlo** | From docx §5.14 | [REQ-STAT-003](../requirements/REQ-STAT-003.md) | `statistics_engine.py` |
| **15 Testing** | From docx §9 | [ATH-002](../ATH-002-Engineering-Standards.md) | `tests/test_backtest_engine_framework.py` |
| **16 Benchmarks** | From docx §10 | [athena-core/benchmarks/](../../athena-core/benchmarks/README.md) | `tests/benchmarks/` |
| **17 AI Coding** | From docx §11 | [AES-0006](../governance/AES-0006-AI-Coding-Standards.md) | — |
| **18 Agent Packages** | From docx §8 | [prompts/](../prompts/) | — |
| **19 Playbooks** | — | [athena-docs/handbook/](../../athena-docs/handbook/) | — |

---

## REQ Traceability (Release-07)

| REQ ID | Section | Module |
|--------|---------|--------|
| REQ-BT-ENGINE-001 | 01 Backtest Engine | `application/backtest_engine.py` |
| REQ-BT-ORDER-001 | 02 Order Engine | `domain/backtest/orders.py` |
| REQ-BT-EXECUTION-001 | 03 Execution Engine | `domain/backtest/execution.py` |
| REQ-WALK-FORWARD-001 | 13 Walk-Forward | `application/walk_forward.py` |
| FR-001 | 01 Backtest Engine | `application/backtest_manager.py` |
| FR-010 | 12 Trade Journal | `domain/backtest/trade_journal.py` |
| FR-011 | 11 Performance Analytics | `backtest_metrics.py` |

# ATH-REL-008 Portfolio Management Engine — Section Index

> **Release package:** [ATH-REL-008-Portfolio-Management-Engine.md](../ATH-REL-008-Portfolio-Management-Engine.md)  
> **Source doc:** `References/REL-008-Portfolio Management Engine.docx`

This index maps the ATH-REL-008 Release-08 module taxonomy to canonical specs and `athena-core` modules.

---

## Section Map

| Section | Doc Status (v0.1) | Canonical Spec | Code / Tooling |
|---------|-------------------|----------------|----------------|
| **00 Executive Summary** | From docx §1 | [ATH-REL-008](../ATH-REL-008-Portfolio-Management-Engine.md) | — |
| **01 Portfolio Framework** | From docx §5.1 | [AES-0900](../portfolio-engine/framework/AES-0900-Portfolio-Engine.md) | `application/portfolio_manager.py` |
| **02 Capital Allocation** | From docx §5.2 | [REQ-PF-ALLOCATION-001](../requirements/REQ-PF-ALLOCATION-001.md) | `domain/portfolio/allocation.py` |
| **03 Position Allocation** | From docx §5.3 | [REQ-PF-003](../portfolio-engine/requirements/REQ-PF-003.md) | `portfolio_risk.py` |
| **04 Risk Budget Engine** | From docx §5.4 | [REQ-PF-RISK-001](../requirements/REQ-PF-RISK-001.md) | `domain/portfolio/risk_budget.py` |
| **05 Exposure Management** | From docx §5.5 | [REQ-PF-001](../portfolio-engine/requirements/REQ-PF-001.md) | `application/portfolio_engine.py` |
| **06 Diversification Engine** | From docx §5.6 | — | `portfolio_risk.py` |
| **07 Correlation Engine** | From docx §5.7 | — | `portfolio_manager.py`, `portfolio_risk.py` |
| **08 Portfolio Rebalancing** | From docx §5.8 | [REQ-PF-002](../portfolio-engine/requirements/REQ-PF-002.md) | `portfolio_engine.py` |
| **09 Cash Management** | From docx §5.9 | — | `portfolio_manager.py` |
| **10 Portfolio Optimization** | From docx §5.10 | — | `application/portfolio_optimizer.py` |
| **11 Portfolio Analytics** | From docx §5.11 | — | `application/portfolio_analytics.py` |
| **12 Multi-Portfolio Management** | From docx §5.12 | — | `application/portfolio_manager.py` |
| **13 Testing** | From docx §9 | [ATH-002](../ATH-002-Engineering-Standards.md) | `tests/test_portfolio_engine_framework.py` |
| **14 Benchmarks** | From docx §10 | [athena-core/benchmarks/](../../athena-core/benchmarks/README.md) | `tests/benchmarks/` |
| **15 AI Coding** | From docx §11 | [AES-0006](../governance/AES-0006-AI-Coding-Standards.md) | — |
| **16 Agent Packages** | From docx §8 | [prompts/](../prompts/) | — |
| **17 Playbooks** | — | [athena-docs/handbook/](../../athena-docs/handbook/) | — |

---

## REQ Traceability (Release-08)

| REQ ID | Section | Module |
|--------|---------|--------|
| REQ-PF-001 | 05 Exposure Management | `application/portfolio_engine.py` |
| REQ-PF-002 | 08 Portfolio Rebalancing | `application/portfolio_engine.py` |
| REQ-PF-003 | 03 Position Allocation | `domain/portfolio/models.py` |
| REQ-PF-ALLOCATION-001 | 02 Capital Allocation | `domain/portfolio/allocation.py` |
| REQ-PF-RISK-001 | 04 Risk Budget Engine | `domain/portfolio/risk_budget.py` |
| REQ-PF-SNAPSHOT-001 | 01 Portfolio Framework | `domain/portfolio/snapshot.py` |
| FR-001 | 12 Multi-Portfolio | `application/portfolio_manager.py` |
| FR-005 | 10 Portfolio Optimization | `application/portfolio_optimizer.py` |
| FR-014 | 01 Portfolio Framework | `domain/portfolio/snapshot.py` |

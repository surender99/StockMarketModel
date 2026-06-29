# ATH-REL-008 – Portfolio Management Engine (Release-08)

> **Version:** v0.1  
> **Source:** `References/REL-008-Portfolio Management Engine.docx`  
> **Status:** Spec-integrated (skeleton release package)  
> **Validation:** [packages/PACKAGE-REL-008-COMPLETE.md](packages/PACKAGE-REL-008-COMPLETE.md)

ATH-REL-008 is the **portfolio management engine release package** for Athena Release-08. It extends Package 09 portfolio engine with multi-portfolio management, capital allocation models, risk budgets, rebalancing, optimization, analytics, and immutable snapshots.

---

## Purpose

| Aspect | Detail |
|--------|--------|
| **What** | Portfolio lifecycle, allocation models, risk budgets, exposure, rebalancing, optimization, analytics |
| **When** | After REL-007 backtesting engine |
| **Who** | `athena-core` developers, portfolio managers, AI coding agents |

Release-08 v0.1 ships as a **skeleton**: the Word document defines module taxonomy; canonical content lives in ATH/AES documents, REQ files, and `athena-core` modules cross-linked from [release-08/](release-08/README.md).

---

## Relationship to Prior Releases

| ID | Role | Canonical Path |
|----|------|----------------|
| **ATH-REL-007** | Backtesting engine | [ATH-REL-007-Backtesting-Engine.md](ATH-REL-007-Backtesting-Engine.md) |
| **Package 09** | Portfolio AES specs | [portfolio-engine/](portfolio-engine/) |
| **AES-0900** | Portfolio engine framework | [AES-0900](portfolio-engine/framework/AES-0900-Portfolio-Engine.md) |
| **AES-0901** | Risk management | Existing `portfolio_risk.py` |

**Reading order:** ATH-REL-007 → Package 09 → ATH-REL-008 (this index) → REQ-PF-*.

---

## Release Package Sections (v0.1)

| # | Section | Doc Module | Canonical Spec / Code |
|---|---------|------------|------------------------|
| 00 | Executive Summary | §1 | This document |
| 01 | Portfolio Framework | §5.1 | `application/portfolio_manager.py`, `domain/portfolio/context.py` |
| 02 | Capital Allocation | §5.2 | `domain/portfolio/allocation.py`, REQ-PF-ALLOCATION-001 |
| 03 | Position Allocation | §5.3 | `portfolio_risk.py` (limits) |
| 04 | Risk Budget Engine | §5.4 | `domain/portfolio/risk_budget.py`, REQ-PF-RISK-001 |
| 05 | Exposure Management | §5.5 | `portfolio_engine.py`, REQ-PF-001 |
| 06 | Diversification Engine | §5.6 | `portfolio_risk.py` (correlation) |
| 07 | Correlation Engine | §5.7 | `portfolio_risk.py`, `portfolio_manager.py` |
| 08 | Portfolio Rebalancing | §5.8 | `portfolio_engine.py`, REQ-PF-002 |
| 09 | Cash Management | §5.9 | `portfolio_manager.py` |
| 10 | Portfolio Optimization | §5.10 | `application/portfolio_optimizer.py` |
| 11 | Portfolio Analytics | §5.11 | `application/portfolio_analytics.py` |
| 12 | Multi-Portfolio Management | §5.12 | `application/portfolio_manager.py` |
| 13 | Testing | §9 | `tests/test_portfolio_engine_framework.py` |
| 14 | Benchmarks | §10 | [athena-core/benchmarks/](../athena-core/benchmarks/README.md) |
| 15 | AI Coding | §11 | [AES-0006](governance/AES-0006-AI-Coding-Standards.md) |
| 16 | Agent Packages | §8 | [prompts/](prompts/) |
| 17 | Playbooks | — | [athena-docs/handbook/](../athena-docs/handbook/) |

Full section index: [release-08/README.md](release-08/README.md).

---

## Functional Requirements (FR-001–FR-015)

| ID | Requirement | v0.1 Status |
|----|-------------|-------------|
| FR-001 | Multiple portfolios | ✅ PortfolioManager |
| FR-002 | Dynamic capital allocation | ✅ compute_allocation_weights |
| FR-003 | Configurable allocation models | ✅ equal_weight, market_cap, risk_weight, volatility_weight, custom |
| FR-004 | Portfolio rebalancing | ✅ PortfolioEngine.suggest_rebalance |
| FR-005 | Portfolio optimization | ✅ inverse_volatility, minimum_variance |
| FR-006 | Portfolio risk budgets | ✅ RiskBudget, passes_risk_budget |
| FR-007 | Exposure calculations | ✅ PortfolioEngine.evaluate |
| FR-008 | Correlation analysis | ✅ correlation_matrix, rolling_correlation |
| FR-009 | Cash management | ✅ reserve_capital, release_capital |
| FR-010 | Sector limits | ✅ PortfolioLimits (existing) |
| FR-011 | Concentration limits | ✅ PortfolioLimits (existing) |
| FR-012 | Multiple currencies | 📋 Deferred |
| FR-013 | Portfolio reporting | 📋 Deferred |
| FR-014 | Portfolio snapshots | ✅ PortfolioSnapshot |
| FR-015 | Portfolio versioning | ✅ PortfolioContext.version |

---

## Implemented vs Documented-Only (v0.1)

| Category | Status | Evidence |
|----------|--------|----------|
| PortfolioManager multi-portfolio | ✅ Implemented | `application/portfolio_manager.py` |
| Allocation model registry | ✅ Implemented | `portfolio_plugins.py`, bootstrap |
| Risk budgets + contributions | ✅ Implemented | `domain/portfolio/risk_budget.py` |
| Portfolio optimization MVP | ✅ Implemented | `portfolio_optimizer.py` |
| Portfolio analytics | ✅ Implemented | `portfolio_analytics.py` |
| Immutable snapshots | ✅ Implemented | `domain/portfolio/snapshot.py` |
| Mean-variance, Black-Litterman, multi-currency | 📋 Documented-only | Deferred |
| Institutional reporting, ESG | 📋 Documented-only | Deferred |

---

## Related Documents

- [ATH-REL-007 Backtesting Engine](ATH-REL-007-Backtesting-Engine.md)
- [contracts/PortfolioProvider.md](portfolio-engine/contracts/PortfolioProvider.md)
- [REQ-PF-ALLOCATION-001](requirements/REQ-PF-ALLOCATION-001.md)
- [REQ-PF-RISK-001](requirements/REQ-PF-RISK-001.md)
- [REQ-PF-SNAPSHOT-001](requirements/REQ-PF-SNAPSHOT-001.md)
- [REFERENCES-INDEX](REFERENCES-INDEX.md)

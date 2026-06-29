# REQ-PF-RISK-001

**Requirement ID:** REQ-PF-RISK-001

**Title:** Portfolio Risk Budget Engine

**Purpose:** Enforce portfolio-level risk budgets including heat, exposure caps, and daily loss limits.

**Acceptance Criteria:**
- [ ] `RiskBudget` defines max heat, gross/net exposure, daily loss
- [ ] `passes_risk_budget` validates portfolio evaluation against budget
- [ ] `risk_contributions` computes per-symbol marginal risk contribution
- [ ] PortfolioManager integrates risk budget checks

**Unit Tests:** `tests/test_portfolio_engine_framework.py`

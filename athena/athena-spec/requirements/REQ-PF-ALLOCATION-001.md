# REQ-PF-ALLOCATION-001

**Requirement ID:** REQ-PF-ALLOCATION-001

**Title:** Capital Allocation Models

**Purpose:** Provide configurable allocation models for dynamic capital deployment across portfolio symbols.

**Acceptance Criteria:**
- [ ] `equal_weight`, `market_cap`, `risk_weight`, `volatility_weight`, and `custom` models supported
- [ ] Weights normalize to sum to 1.0
- [ ] Allocation models registered in PluginRegistry
- [ ] PortfolioManager computes target weights from portfolio config

**Unit Tests:** `tests/test_portfolio_engine_framework.py`

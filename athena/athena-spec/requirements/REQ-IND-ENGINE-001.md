# REQ-IND-ENGINE-001

**Requirement ID:** REQ-IND-ENGINE-001

**Title:** Indicator Execution Engine

**Purpose:** Provide a unified execution layer that resolves indicators from PluginRegistry, runs them against OHLCV, and validates output.

**Acceptance Criteria:**
- [ ] `IndicatorEngine.compute` resolves indicator by ID and returns aligned output
- [ ] `IndicatorEngine.compute_many` runs multiple indicators in one call
- [ ] Output length validated against input OHLCV rows

**Unit Tests:** `tests/test_indicator_framework.py`

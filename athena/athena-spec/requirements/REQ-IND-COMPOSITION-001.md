# REQ-IND-COMPOSITION-001

**Requirement ID:** REQ-IND-COMPOSITION-001

**Title:** Indicator Composition

**Purpose:** Run multiple indicators against the same OHLCV frame in a single engine call.

**Acceptance Criteria:**
- [ ] `IndicatorEngine.compute_many` returns dict keyed by indicator ID
- [ ] Each output passes validation

**Unit Tests:** `tests/test_indicator_framework.py`

# REQ-IND-VALIDATION-001

**Requirement ID:** REQ-IND-VALIDATION-001

**Title:** Indicator Output Validation

**Purpose:** Validate indicator outputs align with input OHLCV row count before caching or downstream use.

**Acceptance Criteria:**
- [ ] `validate_indicator_output` raises on length mismatch
- [ ] Called by `IndicatorEngine.compute`

**Unit Tests:** `tests/test_indicator_framework.py`

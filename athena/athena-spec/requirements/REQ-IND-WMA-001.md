# REQ-IND-WMA-001

**Requirement ID:** REQ-IND-WMA-001

**Title:** Weighted Moving Average (WMA)

**Purpose:** Compute vectorized WMA over a price series for trend analysis.

**Inputs:** OHLCV DataFrame, `period` (int), optional `price_column`

**Outputs:** pandas Series aligned to input rows; NaN during warmup

**Acceptance Criteria:**
- [ ] Registered in indicator plugin registry
- [ ] Available via FeatureService and IndicatorEngine

**Unit Tests:** `tests/test_indicator_framework.py`

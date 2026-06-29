# REQ-IND-ATR-001

**Requirement ID:** REQ-IND-ATR-001

**Title:** Average True Range (ATR) Indicator

**Purpose:** Compute vectorized ATR over OHLCV for volatility sizing, stop placement, and regime classification.

**Description:** ATR measures average true range over a configurable lookback using the standard true-range formula (max of high-low, |high-prev_close|, |low-prev_close|) smoothed with a simple moving average.

**Inputs:**
- OHLCV DataFrame with `high`, `low`, `close`
- `period`: int (default 14)

**Outputs:**
- pandas Series named `atr` aligned to input rows; NaN during warmup

**Acceptance Criteria:**
- [ ] Positive values after warmup period
- [ ] Warmup rows are NaN, not zero-filled
- [ ] Registered in indicator plugin registry (REQ-FEAT-REGISTRY-001)
- [ ] Available via FeatureService and feature pipeline

**Unit Tests:** `tests/test_indicators_atr.py`, `tests/test_feature_engineering_framework.py`

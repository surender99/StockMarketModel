# REQ-IND-ADX-001

**Requirement ID:** REQ-IND-ADX-001

**Title:** Average Directional Index (ADX) Indicator

**Purpose:** Measure trend strength for regime filters and strategy gating.

**Description:** ADX is computed from directional movement (+DM, -DM) and true range over a configurable period. Values range from 0 to 100.

**Inputs:**
- OHLCV DataFrame with `high`, `low`, `close`
- `period`: int (default 14)

**Outputs:**
- pandas Series named `adx`

**Acceptance Criteria:**
- [ ] Values bounded 0–100 after warmup
- [ ] Registered in indicator plugin registry
- [ ] Available via FeatureService

**Unit Tests:** `tests/test_indicators_adx.py`, `tests/test_feature_engineering_framework.py`

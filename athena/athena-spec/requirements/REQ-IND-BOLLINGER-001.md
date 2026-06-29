# REQ-IND-BOLLINGER-001

**Requirement ID:** REQ-IND-BOLLINGER-001

**Title:** Bollinger Bands Indicator

**Purpose:** Provide volatility envelopes around a moving average for mean-reversion and breakout strategies.

**Description:** Bollinger Bands consist of a middle band (SMA), upper band (middle + std_dev × rolling std), and lower band (middle − std_dev × rolling std).

**Inputs:**
- Price series or OHLCV with configurable `price_column`
- `period`: int (default 20)
- `std_dev`: float (default 2.0)

**Outputs:**
- DataFrame with columns `bb_upper`, `bb_middle`, `bb_lower`

**Acceptance Criteria:**
- [ ] Upper ≥ middle ≥ lower after warmup
- [ ] Middle band matches SMA for same period
- [ ] Registered in indicator plugin registry
- [ ] Available via FeatureService

**Unit Tests:** `tests/test_indicators_bollinger.py`, `tests/test_feature_engineering_framework.py`

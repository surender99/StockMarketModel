# REQ-IND-CMF-001

**Requirement ID:** REQ-IND-CMF-001

**Title:** Chaikin Money Flow (CMF)

**Purpose:** Volume-weighted accumulation/distribution over a rolling window.

**Inputs:** OHLCV DataFrame, `period` (default 20)

**Outputs:** pandas Series bounded roughly -1 to +1

**Unit Tests:** `tests/test_indicator_framework.py`

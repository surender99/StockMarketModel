# REQ-IND-CCI-001

**Requirement ID:** REQ-IND-CCI-001

**Title:** Commodity Channel Index (CCI)

**Purpose:** Measure price deviation from statistical mean over a rolling window.

**Inputs:** OHLCV DataFrame, `period` (default 20)

**Outputs:** pandas Series (unbounded oscillator)

**Unit Tests:** `tests/test_indicator_framework.py`

# REQ-IND-OBV-001

**Requirement ID:** REQ-IND-OBV-001

**Title:** On-Balance Volume (OBV)

**Purpose:** Cumulative volume flow indicator based on close direction.

**Inputs:** OHLCV DataFrame with `close`, `volume`

**Outputs:** pandas Series (cumulative OBV)

**Unit Tests:** `tests/test_indicator_framework.py`

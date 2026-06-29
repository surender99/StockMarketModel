# REQ-IND-MFI-001

**Requirement ID:** REQ-IND-MFI-001

**Title:** Money Flow Index (MFI)

**Purpose:** Volume-weighted RSI variant bounded 0–100.

**Inputs:** OHLCV DataFrame, `period` (default 14)

**Outputs:** pandas Series 0–100 after warmup

**Unit Tests:** `tests/test_indicator_framework.py`

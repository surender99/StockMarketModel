# REQ-IND-MACD-001 — MACD Indicator

| Field | Value |
|-------|-------|
| **ID** | REQ-IND-MACD-001 |
| **Title** | MACD, Signal, Histogram |
| **Status** | Implemented |
| **Package** | 05 — Feature Engineering |
| **Defaults** | fast=12, slow=26, signal=9 |

---

## Description

Moving Average Convergence Divergence with signal line and histogram outputs.

---

## Acceptance Criteria

- [x] Returns DataFrame with columns `macd`, `signal`, `histogram`
- [x] Histogram = MACD − Signal
- [x] Registered in `FeatureService` as `macd`
- [x] Parity tests vs pandas-ta when available

---

## Implementation

`athena_core/domain/indicators/macd.py`

# REQ-IND-RSI-001 — RSI Indicator

| Field | Value |
|-------|-------|
| **ID** | REQ-IND-RSI-001 |
| **Title** | Relative Strength Index (Wilder) |
| **Status** | Implemented |
| **Package** | 05 — Feature Engineering |
| **Range** | 0–100 |

---

## Description

Wilder-smoothed RSI for momentum measurement.

---

## Acceptance Criteria

- [x] Output bounded 0–100
- [x] Wilder smoothing (alpha=1/period)
- [x] Registered in `FeatureService` as `rsi`
- [x] Parity tests vs pandas-ta when available

---

## Implementation

`athena_core/domain/indicators/rsi.py`

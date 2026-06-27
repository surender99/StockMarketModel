# REQ-DATA-QUALITY-001 — OHLCV Data Quality Validation

| Field | Value |
|-------|-------|
| **ID** | REQ-DATA-QUALITY-001 |
| **Title** | OHLCV data quality checks before feature generation |
| **Status** | Implemented |
| **Package** | 03 — Data Platform |
| **Spec** | [AES-0310 Data Quality](../data/quality/AES-0310-Data-Quality.md) |

---

## Description

Validate ingested OHLCV data for missing candles, duplicate rows, invalid OHLC relationships, zero-volume anomalies, and return outliers. Produce a `DataQualityReport` before feature generation.

---

## Acceptance Criteria

- [x] `check_ohlcv_quality()` returns `DataQualityReport` with `passed` boolean
- [x] Detects duplicate dates, invalid OHLC, zero volume, outliers
- [x] Empty DataFrame fails with `MISSING_CANDLES`
- [x] Unit tests in `tests/test_data_quality.py`

---

## Implementation

| Layer | Path |
|-------|------|
| Domain | `athena_core/domain/data/quality.py` |

---

## Integration Tests

Optional: call after ingest in integration pipeline (deferred to operator workflow).

---

## Related

- [REQ-DATA-INGEST-001](REQ-DATA-INGEST-001.md)
- [DataProvider](../contracts/DataProvider.md)

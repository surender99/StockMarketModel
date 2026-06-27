# DataProvider Contract

> **References source:** `References/Athena-Package-03-Data-Platform/contracts/DataProvider.md`  
> **Architecture:** [AES-0300 Data Platform](../data/AES-0300-Data-Platform.md)  
> **Implementation:** `athena-core` — `OHLCVRepositoryPort`, `YFinanceClient`, `ParquetOHLCVStore`

Contract for market data providers — deterministic, version-aware OHLCV delivery.

---

## Interface

### Inputs

| Input | Type | Description |
|-------|------|-------------|
| symbol | `str` | Ticker (e.g. `RELIANCE.NS`) |
| timeframe | `str` | Bar interval (MVP: `1d`) |
| date range | `date` start/end | Inclusive query window |

### Output

| Output | Type | Description |
|--------|------|-------------|
| OHLCV | `pd.DataFrame` | Normalized columns per [ohlcv-schema.json](../schemas/ohlcv-schema.json) |

---

## Requirements

| # | Rule | Rationale |
|---|------|-----------|
| 1 | **Deterministic** | Same query → same data for a given `data_version` |
| 2 | **Version aware** | Feature store and OHLCV stores tag `data_version` |
| 3 | **No silent correction** | Quality issues reported via [REQ-DATA-QUALITY-001](../requirements/REQ-DATA-QUALITY-001.md) |
| 4 | **Quality gate** | Run [AES-0310](../data/quality/AES-0310-Data-Quality.md) checks before feature generation |

---

## Live Implementation Mapping

| Contract element | `athena-core` location |
|------------------|------------------------|
| Fetch from source | `infrastructure/yfinance_client.py` |
| Persist OHLCV | `infrastructure/parquet_ohlcv_store.py` |
| Repository port | `domain/ports/ohlcv_repository.py` |
| Ingest use case | `application/ingest_ohlcv.py` |
| Quality checks | `domain/data/quality.py` |

---

## Related Documents

| Document | Purpose |
|----------|---------|
| [REQ-DATA-INGEST-001](../requirements/REQ-DATA-INGEST-001.md) | yfinance ingest |
| [REQ-DATA-CALENDAR-001](../requirements/REQ-DATA-CALENDAR-001.md) | NSE calendar |
| [REQ-DATA-QUALITY-001](../requirements/REQ-DATA-QUALITY-001.md) | Quality validation |

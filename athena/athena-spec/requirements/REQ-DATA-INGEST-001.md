# REQ-DATA-INGEST-001

**Requirement ID:** REQ-DATA-INGEST-001

**Title:** Daily OHLCV Ingestion (yfinance → Parquet)

**Purpose:** Provide a reproducible pipeline to fetch NSE daily OHLCV bars via yfinance and persist them as partitioned Parquet files for downstream indicators and backtesting.

**Description:** The data ingestion module downloads historical daily Open, High, Low, Close, Volume (OHLCV) data for symbols in the NIFTY 500 universe. Data is normalized to a canonical schema, validated, and written to local Parquet storage organized by symbol and date range. The module supports incremental updates (fetch only missing dates) and idempotent writes.

**Inputs:**
- Symbol identifier (e.g. `RELIANCE.NS` for yfinance NSE suffix)
- Date range (`start_date`, `end_date`) in ISO 8601
- Optional: universe list (CSV or config) of NIFTY 500 tickers

**Outputs:**
- Parquet file(s) per symbol under configurable base path, e.g. `data/ohlcv/{symbol}/bars.parquet`
- Ingestion manifest/log entry (symbol, date range, row count, timestamp, source)

**Configuration:**
```yaml
data_ingest:
  source: yfinance
  base_path: ./data/ohlcv
  symbol_suffix: .NS
  bar_frequency: 1d
  retry:
    max_attempts: 3
    backoff_seconds: 2
  schema:
    columns: [date, open, high, low, close, volume, symbol]
```

**Algorithm:**
1. Resolve yfinance ticker from symbol + suffix.
2. Call `yfinance.download()` for the requested date range with `auto_adjust=False` (MVP).
3. Normalize column names to lowercase snake_case.
4. Validate: no duplicate dates, OHLC consistency (high ≥ max(open, close), low ≤ min(open, close)), volume ≥ 0.
5. Merge with existing Parquet if present (incremental); deduplicate by date.
6. Write atomically (temp file + rename) to Parquet with Snappy compression.

**Dependencies:**
- yfinance
- pyarrow / pandas
- REQ-DATA-CALENDAR-001 (optional validation against trading days)

**Acceptance Criteria:**
- [ ] Fetches ≥252 trading days for a liquid NSE symbol (e.g. RELIANCE.NS)
- [ ] Output schema matches configured columns exactly
- [ ] Incremental re-run does not duplicate rows
- [ ] Missing yfinance data raises a structured error with symbol and date range
- [ ] All dates stored as timezone-naive date (NSE local session date)

**Performance Target:**
- Single symbol, 5 years daily: < 5 seconds end-to-end on typical broadband
- Batch 10 symbols: < 30 seconds

**Unit Tests:**
- Schema normalization from mock yfinance response
- OHLC validation rejects invalid bars
- Incremental merge deduplication
- Empty response handling

**Integration Tests:**
- Live fetch for one symbol (marked `@pytest.mark.integration`, skippable in CI)

**Future Enhancements:**
- Corporate actions adjustment
- Alternative sources (NSE official, broker APIs)
- Async parallel batch ingestion
- DuckDB/Polars backend option

# REQ-IND-EMA-001

**Requirement ID:** REQ-IND-EMA-001

**Title:** Exponential Moving Average (EMA) Indicator

**Purpose:** Compute vectorized EMA over OHLCV price series for use in strategies, features, and backtests with configurable periods and reproducible results.

**Description:** The EMA indicator accepts a price series (typically `close`) and one or more lookback periods. It returns aligned EMA values using the standard exponential smoothing formula with `adjust=False` to match industry libraries (pandas-ta). Implementation lives in the domain/application layer; no strategy-specific thresholds are hardcoded.

**Inputs:**
- `series`: pandas Series of float prices, DatetimeIndex or date column aligned
- `period`: int or list[int] of lookback periods (e.g. 9, 21, 50)
- Optional `price_column` when input is OHLCV DataFrame

**Outputs:**
- pandas Series (single period) or DataFrame (multiple periods) with column names `ema_{period}`
- NaN for initial warmup rows (< period bars)

**Configuration:**
```yaml
indicators:
  ema:
    default_periods: [9, 21, 50, 200]
    price_column: close
    min_periods: null  # defaults to period
```

**Algorithm:**
```
EMA_t = α * Price_t + (1 - α) * EMA_{t-1}
where α = 2 / (period + 1)
```
Use `pandas.Series.ewm(span=period, adjust=False).mean()`.

**Dependencies:**
- pandas, numpy
- REQ-DATA-INGEST-001 (OHLCV input)
- REQ-FEAT-STORE-001 (optional persistence)

**Acceptance Criteria:**
- [ ] Matches pandas-ta `ema` within 1e-6 relative tolerance for same period and price series
- [ ] Supports configurable periods via parameter or config
- [ ] Vectorized — no Python row loops over the series
- [ ] Warmup period produces NaN, not zero-filled values
- [ ] Works on ≥10,000 bar series without memory blow-up

**Performance Target:**
- 10,000 bars, 4 periods: < 50 ms

**Unit Tests:**
- Compare against pandas-ta for periods 9, 21, 50 on synthetic and real sample data
- Single-bar and empty series edge cases
- Multi-period column naming

**Integration Tests:**
- EMA computed from Parquet OHLCV output of REQ-DATA-INGEST-001

**Future Enhancements:**
- Polars backend
- GPU acceleration (optional)
- Register as plugin in indicator registry

# REQ-IND-SMA-001

**Requirement ID:** REQ-IND-SMA-001

**Title:** Simple Moving Average (SMA) Indicator

**Purpose:** Compute vectorized SMA over OHLCV price series for trend analysis and strategy rules with configurable periods.

**Description:** The SMA indicator calculates the arithmetic mean of the last N prices using a rolling window. It supports single or multiple periods and integrates with the feature store for caching. No strategy entry/exit logic is embedded in the indicator module.

**Inputs:**
- `series`: pandas Series of float prices
- `period`: int or list[int] (e.g. 20, 50, 200)
- Optional `price_column` for OHLCV DataFrame input

**Outputs:**
- pandas Series or DataFrame with columns `sma_{period}`
- NaN during warmup (< period bars)

**Configuration:**
```yaml
indicators:
  sma:
    default_periods: [20, 50, 200]
    price_column: close
    min_periods: null
```

**Algorithm:**
```
SMA_t = mean(Price_{t-period+1}, ..., Price_t)
```
Use `pandas.Series.rolling(window=period, min_periods=period).mean()`.

**Dependencies:**
- pandas, numpy
- REQ-DATA-INGEST-001
- REQ-FEAT-STORE-001 (optional)

**Acceptance Criteria:**
- [ ] Matches pandas-ta `sma` within 1e-6 absolute tolerance
- [ ] Configurable periods
- [ ] Vectorized implementation
- [ ] NaN during warmup, not forward-filled by default

**Performance Target:**
- 10,000 bars, 3 periods: < 30 ms

**Unit Tests:**
- pandas-ta parity for periods 20, 50, 200
- Period > series length returns all NaN
- Multi-period output shape

**Integration Tests:**
- SMA from ingested Parquet OHLCV

**Future Enhancements:**
- Weighted SMA variants
- Plugin registration alongside EMA

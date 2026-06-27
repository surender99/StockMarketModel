# REQ-REGIME-001

**Requirement ID:** REQ-REGIME-001

**Title:** Market Regime Classification Engine

**Purpose:** Classify market conditions (trend and volatility) to enable regime-conditional strategy filters and explainable scan context.

**Description:** The regime engine analyzes benchmark/index and symbol OHLCV using EMA, ADX, ATR, rolling volatility, and NIFTY trend to label each trading day as bull/bear/sideways and high/low volatility. Strategies may declare regime-conditional filter blocks that gate entries when the active regime is not allowed.

**Inputs:**
- OHLCV DataFrame (symbol or benchmark)
- Regime configuration (thresholds, lookback periods)
- Optional NIFTY benchmark series for market-wide trend context

**Outputs:**
- `RegimeState` per as-of date: trend, volatility, indicator values
- Time series of regime labels for backtest/scanner integration

**Configuration:**
```yaml
regime:
  benchmark_symbol: ^NSEI
  ema_fast_period: 50
  ema_slow_period: 200
  adx_period: 14
  adx_sideways_threshold: 20
  atr_period: 14
  rolling_vol_window: 20
  vol_high_percentile: 0.75
  vol_lookback_days: 252
```

**Algorithm:**
1. Compute EMA fast/slow, ADX, ATR%, and rolling volatility on benchmark OHLCV.
2. Trend: bull if close > EMA slow and EMA fast > EMA slow; bear if close < EMA slow and EMA fast < EMA slow; else sideways (or ADX below threshold).
3. Volatility: high if rolling vol exceeds historical percentile threshold; else low.
4. Attach NIFTY trend label from benchmark classification.
5. Strategy filters consult active regime at entry evaluation time (no lookahead).

**Dependencies:**
- REQ-DATA-INGEST-001, REQ-DATA-CALENDAR-001
- REQ-IND-EMA-001
- REQ-STRAT-CONFIG-001 (regime-conditional filters)

**Acceptance Criteria:**
- [ ] Classifies synthetic bull/bear/sideways series correctly
- [ ] High/low volatility separation on synthetic vol spike series
- [ ] Regime at day t uses only data with date ≤ t
- [ ] Strategy regime filters block entries when regime disallowed
- [ ] Configurable thresholds via YAML/Pydantic

**Unit Tests:**
- Bull trend detection on rising EMA stack
- Sideways when ADX low
- Vol regime flip on synthetic spike
- Regime filter integration in backtest engine

**Future Enhancements:**
- Sector-relative regime
- ML-based regime clustering

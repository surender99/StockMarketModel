# REQ-BT-ENGINE-001

**Requirement ID:** REQ-BT-ENGINE-001

**Title:** Backtest Engine with Transaction Costs

**Purpose:** Simulate portfolio performance of a configuration-driven strategy over historical OHLCV with realistic costs, position constraints, and benchmark comparison.

**Description:** The backtest engine walks forward day-by-day (no lookahead), evaluates strategy rules using only data available at each bar, executes simulated trades with configurable brokerage, slippage, and taxes, and produces trade log, equity curve, and summary metrics. It consumes `StrategyConfig` from REQ-STRAT-CONFIG-001 and OHLCV/features from the data layer.

**Inputs:**
- `StrategyConfig` (from YAML)
- OHLCV + precomputed features for universe and date range
- Backtest settings (capital, costs, benchmark symbol)

**Outputs:**
- Trade log (entry/exit date, symbol, price, qty, fees, P&L)
- Daily equity curve
- Summary metrics: total return, CAGR, max drawdown, Sharpe, win rate, profit factor
- Benchmark comparison metrics

**Configuration:**
```yaml
backtest:
  initial_capital: 1000000
  currency: INR
  costs:
    brokerage_pct: 0.0003
    brokerage_flat: 20
    slippage_pct: 0.001
    stt_pct: 0.001
    gst_on_brokerage_pct: 0.18
  benchmark: ^NSEI  # NIFTY 50
  fill_price: close  # MVP: close-of-bar fills
  allow_fractional: false
```

**Algorithm:**
1. Initialize portfolio: cash = initial_capital, positions = {}.
2. For each trading day t in calendar order (REQ-DATA-CALENDAR-001):
   a. Build feature snapshot using data ≤ t only.
   b. Evaluate exit rules for open positions; simulate fills at configured price + slippage.
   c. Evaluate entry rules for universe; apply filters and max_positions cap.
   d. Apply position sizing; deduct costs on entry.
   e. Record equity = cash + mark-to-market positions.
3. Compute metrics from equity curve and trade log.
4. Run benchmark buy-and-hold over same period for comparison.

**Dependencies:**
- REQ-STRAT-CONFIG-001
- REQ-DATA-INGEST-001, REQ-DATA-CALENDAR-001
- REQ-IND-*, REQ-FEAT-STORE-001
- REQ-EXP-TRACK-001 (optional persist results)

**Acceptance Criteria:**
- [ ] No lookahead: features at day t use only data with date ≤ t
- [ ] Costs reduce net P&L vs zero-cost run
- [ ] Respects `max_positions` and capital constraints
- [ ] Trade log row count matches executed entries/exits
- [ ] Reproducible: same inputs → identical trade log and metrics
- [ ] Benchmark metrics computed for same date range

**Performance Target:**
- 1 symbol, 5 years daily, simple strategy: < 2 seconds
- 50 symbols, 3 years: < 30 seconds (MVP target)

**Unit Tests:**
- Known synthetic price series → expected trade count
- Cost calculation spot checks (brokerage + slippage)
- Max positions enforced
- Lookahead detection test (shifted signal must not trade early)

**Integration Tests:**
- End-to-end: ingest → EMA → strategy YAML → backtest → metrics

**Future Enhancements:**
- Walk-forward validation framework
- Open-to-close vs close-to-close fill models
- Short selling, margin
- Multi-strategy portfolio backtest

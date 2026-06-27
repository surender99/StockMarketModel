# REQ-WALK-FORWARD-001

**Requirement ID:** REQ-WALK-FORWARD-001

**Title:** Walk-Forward Validation Framework

**Purpose:** Formalize train/test window splitting and aggregate out-of-sample metrics across multiple folds integrated with the backtest engine.

**Description:** Walk-forward validation generates sequential train/test windows over a date range, runs the backtest engine on each test window (using only that window's dates for simulation), optionally records experiments per fold, and aggregates fold metrics (mean, std, min, max) for robust strategy evaluation.

**Inputs:**
- `StrategyConfig`, symbol universe
- Full date range and window parameters (train_days, test_days, step_days, mode)
- Backtest engine and calendar

**Outputs:**
- List of per-fold `WalkForwardFoldResult` (train/test ranges, metrics)
- Aggregated summary metrics across folds

**Configuration:**
```yaml
walk_forward:
  train_days: 252
  test_days: 63
  step_days: 63
  mode: rolling  # rolling | expanding
  min_train_days: 126
```

**Algorithm:**
1. Enumerate trading days in [start, end].
2. Generate folds: each fold has train [t0, t1) and test [t1, t2) per mode/step.
3. For each fold, run `BacktestEngine.run` on test window only.
4. Collect metrics per fold; compute aggregate statistics.
5. Optionally persist experiment record per fold via REQ-EXP-TRACK-001.

**Dependencies:**
- REQ-BT-ENGINE-001, REQ-DATA-CALENDAR-001
- REQ-EXP-TRACK-001 (optional)

**Acceptance Criteria:**
- [ ] Generates non-overlapping test windows per configuration
- [ ] Each fold backtest uses only its test date range
- [ ] Aggregate metrics computed across folds
- [ ] Reproducible fold boundaries for same inputs
- [ ] CLI `walk-forward` command integrated

**Unit Tests:**
- Fold count for known calendar length
- Test window dates do not overlap (rolling mode)
- Aggregate metrics on synthetic folds

**Future Enhancements:**
- Parameter optimization on train window (Phase 4)
- Purged/embargo splits for ML features

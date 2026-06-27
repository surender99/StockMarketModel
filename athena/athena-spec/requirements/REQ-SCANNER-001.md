# REQ-SCANNER-001

**Requirement ID:** REQ-SCANNER-001

**Title:** Daily Universe Scanner

**Purpose:** Batch-evaluate a symbol universe against active strategy rules and rank top candidates for the trading day with explainable scoring.

**Description:** The daily scanner loads NIFTY 500 (or custom) symbols, evaluates entry signals and scoring dimensions (breakout proximity, relative strength vs benchmark, momentum, composite probability), applies regime and volume filters, and outputs the top N candidates with human-readable reasons.

**Inputs:**
- Strategy YAML (`StrategyConfig`)
- Symbol universe (CSV or config)
- As-of scan date
- OHLCV + features from feature store
- Optional regime state from REQ-REGIME-001

**Outputs:**
- Ranked list of `ScanCandidate` records: symbol, score, reasons, signal flags
- JSON/CLI table output

**Configuration:**
```yaml
scanner:
  top_n: 20
  min_score: 0.0
  weights:
    breakout: 0.25
    relative_strength: 0.25
    momentum: 0.25
    signal_probability: 0.25
  breakout_lookback_days: 252
  momentum_lookback_days: 20
  rs_lookback_days: 63
```

**Algorithm:**
1. For each symbol, load OHLCV through as-of date.
2. Evaluate strategy entry rules and standard filters (volume, regime).
3. Score breakout (close / N-day high), RS (symbol return vs benchmark), momentum (N-day ROC), signal probability (normalized composite).
4. Sort descending by composite score; truncate to top N.
5. Attach explainable reason strings per dimension.

**Dependencies:**
- REQ-STRAT-CONFIG-001, REQ-BT-ENGINE-001 (shared filter/eval logic)
- REQ-FEAT-STORE-001, REQ-REGIME-001

**Acceptance Criteria:**
- [ ] Ranks symbols with higher momentum/RS above lower on synthetic data
- [ ] Respects top_n limit
- [ ] Each candidate includes at least one reason string
- [ ] Skips symbols failing volume/regime filters
- [ ] CLI `scan` command produces JSON output

**Unit Tests:**
- Synthetic ranking order
- Filter exclusion
- Reason string generation
- Empty universe handling

**Future Enhancements:**
- ML probability scorer (Phase 4)
- Intraday scan cadence

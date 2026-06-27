# REQ-ML-SCORER-001

**Requirement ID:** REQ-ML-SCORER-001

**Title:** ML Signal Scorer

**Purpose:** Train a classifier to score the probability of success for strategy-generated entry signals; augment or replace heuristic scanner signal probability.

**Description:** The ML signal scorer trains on labeled backtest trades paired with entry-time feature vectors (breakout, RS, momentum, volume). At scan time it scores only symbols with active strategy entry signals — it never creates new trades or signals.

**Inputs:**
- Labeled training samples from backtest trades + entry features
- Scanner dimension scores at signal time

**Outputs:**
- `SignalScore`: probability of success, confidence, model version
- Augmented `ScanCandidate` fields: `ml_probability`, `ml_confidence`

**Configuration:**
```yaml
ml_scorer:
  enabled: false
  model_type: logistic  # logistic | random_forest
  min_training_samples: 20
  probability_threshold: 0.5
  use_heuristic_fallback: true
  feature_names:
    - breakout_score
    - rs_score
    - momentum_score
    - volume_ratio
    - holding_days_norm

scanner:
  use_ml_scorer: true
```

**Algorithm:**
1. Extract feature vectors at strategy entry signal points from backtests.
2. Label trades: win (net_pnl > 0) = 1, loss = 0.
3. Train sklearn classifier (logistic or random forest) with standard scaling.
4. At scan time, score only candidates with `has_entry_signal=True`.
5. Use ML probability as `signal_probability` weight input; fall back to heuristic if untrained.

**Dependencies:**
- REQ-SCANNER-001, REQ-BT-ENGINE-001

**Acceptance Criteria:**
- [ ] Trains on labeled strategy signal samples
- [ ] Returns probability and confidence in [0, 1]
- [ ] Never generates trades or entry signals
- [ ] Integrates with scanner when `use_ml_scorer` enabled
- [ ] Heuristic fallback when model untrained

**Unit Tests:**
- Training and scoring
- fit_from_trades alignment
- Insufficient sample error
- No trade generation API

**Future Enhancements:**
- Model persistence to `model_path`
- Online retraining pipeline

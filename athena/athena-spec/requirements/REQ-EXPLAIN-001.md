# REQ-EXPLAIN-001

**Requirement ID:** REQ-EXPLAIN-001

**Title:** SHAP Explainability for ML Signal Scores

**Purpose:** Provide feature attribution and plain-English rationale for ML signal scorer outputs in scan results.

**Description:** SHAP (SHapley Additive exPlanations) values attribute each feature's contribution to the predicted success probability. Results are surfaced as structured attributions and human-readable rationale strings appended to scan candidate reasons.

**Inputs:**
- Trained `MLSignalScorer` model
- `SignalFeatures` at scan time

**Outputs:**
- `ExplanationResult`: probability, confidence, feature attributions, rationale string
- `ScanCandidate.ml_rationale` in scanner output

**Configuration:**
```yaml
explainability:
  enabled: true
  top_features: 3
  min_shap_magnitude: 0.01
  include_negative_factors: true
```

**Algorithm:**
1. Score signal with ML scorer.
2. Compute SHAP values via LinearExplainer (logistic) or TreeExplainer (random forest).
3. Rank features by absolute SHAP magnitude; filter by minimum threshold.
4. Build plain-English rationale from top positive/negative drivers.
5. Attach rationale to scan candidate reasons.

**Dependencies:**
- REQ-ML-SCORER-001

**Acceptance Criteria:**
- [ ] Returns rationale string for scored signals
- [ ] Feature attributions include human-readable labels
- [ ] Graceful fallback to heuristic rationale when model untrained or SHAP unavailable
- [ ] Integrated with scanner JSON output via `ml_rationale`

**Unit Tests:**
- Rationale generation for trained model
- Heuristic fallback when untrained
- Attribution list populated

**Future Enhancements:**
- Waterfall plot export for dashboard (Phase 5)
- Batch explanation for full universe scan

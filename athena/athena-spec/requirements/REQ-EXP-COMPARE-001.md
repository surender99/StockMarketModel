# REQ-EXP-COMPARE-001

**Requirement ID:** REQ-EXP-COMPARE-001

**Title:** Experiment Comparison CLI

**Purpose:** Compare side-by-side metrics from persisted experiment records for strategy selection and research review.

**Description:** The comparison tooling loads experiment records by ID or from the experiment index, aligns key metrics in a tabular view, and outputs formatted text or JSON for CLI consumption.

**Inputs:**
- Experiment IDs (2+) or `--latest N` from index
- Experiments directory (`experiment_tracking.base_path`)

**Outputs:**
- Comparison table: experiment_id, strategy_id, periods, selected metrics
- JSON payload for programmatic use

**Configuration:**
```yaml
experiment_tracking:
  base_path: ./experiments
  compare_metrics:
    - total_return
    - cagr
    - max_drawdown
    - sharpe
    - win_rate
    - trade_count
```

**Algorithm:**
1. Load experiment JSON files by ID or from index manifest.
2. Extract configured metric keys (fallback to common defaults).
3. Build aligned rows; highlight missing metrics as null.
4. Render table to stdout or write JSON to `--output`.

**Dependencies:**
- REQ-EXP-TRACK-001

**Acceptance Criteria:**
- [ ] Compares ≥2 experiments by ID
- [ ] `--latest N` selects recent experiments from index
- [ ] Side-by-side metrics aligned in output
- [ ] Missing experiment ID raises clear error
- [ ] Valid JSON output when `--format json`

**Unit Tests:**
- Two-record comparison
- Latest N selection
- Missing ID error handling

**Future Enhancements:**
- HTML report export
- Statistical significance tests between runs

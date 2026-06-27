# REQ-EXP-TRACK-001

**Requirement ID:** REQ-EXP-TRACK-001

**Title:** Experiment Metadata Tracking

**Purpose:** Record sufficient metadata for every backtest or research run so experiments are reproducible, comparable, and auditable.

**Description:** Each experiment run persists a structured record containing strategy identity, dataset version, time periods, indicator parameters, backtest settings, result metrics, artifact paths, git commit hash, and timestamp. Records are stored as JSON (one file per experiment) under a configurable experiments directory and can be listed/filtered for comparison.

**Inputs:**
- Experiment run context: strategy config, backtest config, date ranges
- Results: metrics dict, paths to trade log and equity curve
- Environment: git commit (auto-detected), Python version, athena-core version

**Outputs:**
- Experiment record JSON file, e.g. `experiments/{experiment_id}.json`
- Optional index manifest for listing recent experiments

**Configuration:**
```yaml
experiment_tracking:
  base_path: ./experiments
  auto_capture_git: true
  required_fields:
    - strategy_id
    - strategy_version
    - dataset_version
    - train_start
    - train_end
    - metrics
    - git_commit
    - created_at
```

**Algorithm:**
1. Generate `experiment_id = {timestamp}_{strategy_id}_{short_hash}`.
2. Collect metadata from run context and `git rev-parse HEAD` (if repo available).
3. Attach metrics and artifact relative paths.
4. Validate required fields present.
5. Write JSON atomically to `{base_path}/{experiment_id}.json`.
6. Append to index file (optional).

**Dependencies:**
- pydantic (ExperimentRecord model)
- REQ-BT-ENGINE-001 (primary producer of runs)
- Git CLI or gitpython (optional, graceful fallback if not a git repo)

**Acceptance Criteria:**
- [ ] Every backtest run can optionally persist an experiment record
- [ ] Record includes strategy_id, version, dataset_version, periods, metrics, git_commit, timestamp
- [ ] Same inputs reproduced on different machines differ only by timestamp/experiment_id
- [ ] Missing git repo stores `git_commit: null` with warning log, not failure
- [ ] Records are valid JSON loadable by comparison tooling

**Performance Target:**
- Write experiment record: < 50 ms

**Unit Tests:**
- Record serialization/deserialization
- Required field validation
- Git commit capture mocked
- experiment_id uniqueness (timestamp + hash)

**Integration Tests:**
- Backtest run → experiment file exists with expected metrics keys

**Future Enhancements:**
- MLflow / W&B adapter
- Side-by-side experiment comparison CLI
- Notes and tags fields
- Chart artifact attachments

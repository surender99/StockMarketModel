# REQ-SDK-001

**Requirement ID:** REQ-SDK-001

**Title:** Athena Python SDK

**Purpose:** Expose programmatic access to scan, backtest, walk-forward, optimize, and experiment comparison without invoking the CLI.

**Description:** The `athena-sdk` package provides `AthenaClient`, a thin facade over `AthenaRuntime` in athena-core. Methods return typed domain/application objects with optional `*_dict` helpers for JSON-serializable payloads.

**Inputs:**
- Config path and optional profile
- Strategy YAML path or `StrategyConfig`
- Date ranges, symbol lists, experiment IDs

**Outputs:**
- `ScanResult`, `BacktestRunResult`, `WalkForwardSummary`, `OptimizerResult`
- Dict serializers for CLI/dashboard consumption

**Configuration:** Same Athena YAML as CLI (`AthenaConfig` + profiles).

**Algorithm:**
1. Load config via `load_athena_config`.
2. Lazily construct infrastructure services inside `AthenaRuntime`.
3. Invoke application use cases (scanner, backtest engine, walk-forward, optimizer, experiment tracker).

**Dependencies:**
- athena-core application/runtime layer
- Phase 0–4 use cases

**Acceptance Criteria:**
- [ ] `AthenaClient` supports scan, backtest, walk_forward, optimize, compare_experiments, ingest
- [ ] Config profiles load via constructor `profile=` argument
- [ ] `scan_dict`, `walk_forward_dict`, `optimize_dict` return JSON-ready structures
- [ ] Strategy path or object accepted for strategy-bearing methods

**Unit Tests:**
- Config loading and profile listing

**Future Enhancements:**
- Async client
- REST/gRPC transport adapter

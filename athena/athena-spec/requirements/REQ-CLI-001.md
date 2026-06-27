# REQ-CLI-001

**Requirement ID:** REQ-CLI-001

**Title:** Polished Athena CLI

**Purpose:** Provide a unified command-line experience with consistent flags, config profiles, and structured output across ingest, scan, backtest, walk-forward, optimize, and compare-experiments.

**Description:** The `athena-cli` package exposes the `athena` entrypoint. It wraps `athena-sdk` / `athena-core` runtime helpers with global `--config`, `--profile`, `--output-format`, and per-command `--output` options. Config profiles are named overlays declared under `profiles:` in YAML.

**Inputs:**
- Subcommand and command-specific flags
- Optional `--config` YAML path
- Optional `--profile` name
- Symbol overrides (`--symbol`, `--symbols-file`)

**Outputs:**
- JSON (default) or table (compare-experiments) to stdout or `--output`
- Non-zero exit code on validation or runtime failures

**Configuration:**
```yaml
profiles:
  paper:
    backtest:
      initial_capital: 500000
default_profile: paper
```

**Algorithm:**
1. Parse global CLI flags and selected subcommand.
2. Construct `AthenaClient` with config path and profile.
3. Delegate to SDK methods and render output via shared formatters.
4. `profiles` subcommand lists names from config YAML.

**Dependencies:**
- REQ-SDK-001
- All Phase 0–4 CLI use cases

**Acceptance Criteria:**
- [ ] `athena` entrypoint registers ingest/scan/backtest/walk-forward/optimize/compare-experiments
- [ ] Global `--config` and `--profile` apply to all commands
- [ ] `--output-format json|table` supported where applicable
- [ ] `athena profiles` lists profile names from YAML
- [ ] Unknown profile raises clear error at runtime

**Unit Tests:**
- Parser includes all commands
- Health and profiles smoke tests

**Future Enhancements:**
- Shell completion
- Rich terminal tables and progress bars

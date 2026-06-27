# Changelog

All notable changes to the Athena platform are documented here.

## [1.0.0] — 2026-06-27

### Platform complete

- Phases 0–6 delivered: data ingest, indicators, backtest, walk-forward, regime/scanner, optimizer/ML/SHAP, CLI/SDK/dashboard, AI assistant
- GitHub Actions CI: pytest across all packages on Python 3.11 and 3.12
- One-command install scripts: `athena/scripts/install.ps1`, `athena/scripts/install.sh`, `athena/Makefile`
- ML signal scorer model persistence via `model_path` (joblib save/load)
- Optuna TPE integration for Bayesian optimizer (`optimizer.use_optuna`, optional `[optimizer]` extra)
- Master sign-off: `athena/athena-spec/PLATFORM-COMPLETE.md`

### Packages

| Package | Version | Entry points |
|---------|---------|--------------|
| athena-core | 0.1.0 | `athena-core` |
| athena-sdk | 0.1.0 | — |
| athena-cli | 0.1.0 | `athena` |
| athena-dashboard | 0.1.0 | `athena-dashboard` |
| athena-ai | 0.1.0 | `athena-ai` |

### Testing

- **133+ unit tests** across monorepo (integration tests excluded by default; run with `pytest -m integration`)

## [0.1.0] — 2026-06-27

Initial MVP releases through Phase 6 (commit `da280e6`).

# Golden Datasets

Canonical golden datasets for Athena validation live in:

**`athena-spec/ATHENA/Golden-Datasets/`**

## Available Fixtures (spec)

| File | Purpose |
|------|---------|
| `ohlcv-sample-30d.csv` | 30-day OHLCV sample |
| `ohlcv-dirty-sample.csv` | Data quality validation |
| `symbols-sample.csv` | Symbol master sample |
| `config-minimal.yaml` | Minimal config fixture |
| `ohlcv-sample-30d.parquet` | Parquet OHLCV sample (local copy) |

## Local Copies

This directory may contain parquet/CSV copies for CI. Prefer spec paths via `athena_testing.golden.resolve_golden_dataset()`.

## APS Validation

Link golden datasets in APS traceability blocks. See [TRACEABILITY-INDEX.md](../../athena-spec/ATHENA/APS/TRACEABILITY-INDEX.md).

# athena-examples

Sample configs and symbol lists for Athena Phase 1 development.

## Contents

| Path | Purpose |
|------|---------|
| `symbols/nifty500_sample.csv` | 10-symbol NIFTY 500 subset for dev/testing |
| `config/ingest.yaml` | Sample ingest + feature store configuration |

## Quick start

From repo root after `pip install -e "athena/athena-core[dev]"`:

```bash
cd athena/athena-examples
athena-core ingest \
  --config config/ingest.yaml \
  --symbols-file symbols/nifty500_sample.csv \
  --start 2023-01-01 \
  --end 2024-12-31
```

Single symbol:

```bash
athena-core ingest --symbol RELIANCE --start 2023-01-01 --end 2024-12-31
```

Phase 2 will add example strategy YAML (REQ-STRAT-CONFIG-001) and end-to-end backtest notebooks.

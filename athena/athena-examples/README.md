# athena-examples

Sample configs, strategies, and symbol lists for Athena development.

## Contents

| Path | Purpose |
|------|---------|
| `symbols/nifty500_sample.csv` | 10-symbol NIFTY 500 subset for dev/testing |
| `config/ingest.yaml` | Sample ingest + feature store configuration |
| `config/ema_crossover.yaml` | EMA 50/200 golden-cross strategy (REQ-STRAT-CONFIG-001) |
| `config/backtest.yaml` | Backtest costs, capital, experiment tracking |

## Quick start — ingest

From repo root after `pip install -e "athena/athena-core[dev]"`:

```bash
cd athena/athena-examples
athena-core ingest \
  --config config/ingest.yaml \
  --symbols-file symbols/nifty500_sample.csv \
  --start 2023-01-01 \
  --end 2024-12-31
```

## Quick start — backtest

After OHLCV is ingested under `./data/ohlcv/`:

```bash
athena-core backtest \
  --config config/backtest.yaml \
  --strategy config/ema_crossover.yaml \
  --symbols-file symbols/nifty500_sample.csv \
  --start 2023-01-01 \
  --end 2024-12-31 \
  --output ./runs/latest \
  --track-experiment
```

Single symbol:

```bash
athena-core backtest \
  --config config/backtest.yaml \
  --strategy config/ema_crossover.yaml \
  --symbol RELIANCE \
  --start 2023-01-01 \
  --end 2024-12-31
```

# athena-cli

Polished command-line interface for Athena — **REQ-CLI-001**.

## Install

```bash
cd athena/athena-core && pip install -e ".[dev]"
cd ../athena-sdk && pip install -e ".[dev]"
cd ../athena-cli && pip install -e ".[dev]"
```

## Usage

```bash
# List config profiles
athena profiles --config ../athena-examples/config/backtest.yaml

# Scan with profile overlay
athena scan --strategy ../athena-examples/config/ema_crossover.yaml \
  --as-of 2024-06-01 --config ../athena-examples/config/backtest.yaml \
  --profile paper --output scan.json

# Compare experiments as table
athena compare-experiments --latest 3 \
  --config ../athena-examples/config/backtest.yaml --output-format table
```

Global flags: `--config`, `--profile`, `--output-format json|table`, `-v`.

Legacy entrypoint `athena-core` remains available in the core package.

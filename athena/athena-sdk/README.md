# athena-sdk

Programmatic Python API for Athena — **REQ-SDK-001**.

## Install

```bash
cd athena/athena-core && pip install -e ".[dev]"
cd ../athena-sdk && pip install -e ".[dev]"
```

## Usage

```python
from datetime import date
from athena_sdk import AthenaClient

client = AthenaClient(
    config_path="../athena-examples/config/backtest.yaml",
    profile="paper",
)

payload = client.scan_dict(
    "../athena-examples/config/ema_crossover.yaml",
    date(2024, 6, 1),
)
print(payload["candidates"][:3])
```

See `AthenaClient` for `backtest`, `walk_forward`, `optimize`, and `compare_experiments`.

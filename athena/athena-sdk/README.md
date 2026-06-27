# athena-sdk

Programmatic Python API for Athena — **REQ-SDK-001**.

## Public API boundary

**`AthenaClient`** is the only supported import for application code:

```python
from athena_sdk import AthenaClient
```

- Do **not** import `athena_core` directly from apps, CLI extensions, or notebooks — use `AthenaClient` methods instead.
- `athena_core.application.*` imports inside `client.py` are **internal** wiring; they may change without semver guarantees on those modules.
- Version: `athena_sdk.__version__` (aligned with package release; see `pyproject.toml`).

See also [ATH-003 Repository Architecture](../athena-spec/ATH-003-Repository-Architecture.md) — interfaces layer.

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

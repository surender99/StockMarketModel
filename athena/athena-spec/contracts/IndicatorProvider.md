# IndicatorProvider Contract

> **References source:** `References/Athena-Package-02-Architecture/contracts/IndicatorProvider.md`  
> **Architecture:** [AES-0202 Plugin Architecture](../architecture/AES-0202-Plugin-Architecture.md)  
> **Implementation:** `athena-core/src/athena_core/domain/indicators/`, `application/feature_service.py`

Contract for indicator plugins — pure, deterministic feature computation from OHLCV data.

---

## Interface

### Inputs

| Input | Type | Description |
|-------|------|-------------|
| OHLCV | `pd.DataFrame` | Columns: `date`, `open`, `high`, `low`, `close`, `volume` |
| Parameters | `dict[str, Any]` | Indicator-specific (e.g. `period`, `price_column`) |

### Outputs

| Output | Type | Description |
|--------|------|-------------|
| Values | `pd.Series` or `pd.DataFrame` | One or more feature columns aligned to input index |

---

## Requirements

| # | Rule | Rationale |
|---|------|-----------|
| 1 | **Pure function** | Same inputs → same outputs; no side effects |
| 2 | **Deterministic** | Reproducible across runs and environments |
| 3 | **Vectorized** | Pandas/numpy operations — no Python loops over bars |
| 4 | **No future data** | No lookahead; each row uses only data available at that bar |

---

## Live Implementation Mapping

| Contract element | `athena-core` location |
|------------------|------------------------|
| Pure compute functions | `domain/indicators/ema.py`, `domain/indicators/sma.py` |
| OHLCV → feature adapter | `compute_*_from_ohlcv()` helpers |
| Registry lookup | `FeatureService._INDICATOR_REGISTRY` (`feature_id` → callable) |
| Cache layer | `FeatureService.get_feature()` via `FeatureStorePort` |
| Config schema | `IndicatorSpec` in `domain/strategy/config.py` |

### Example: EMA

```python
# domain/indicators/ema.py
def compute_ema_from_ohlcv(
    df: pd.DataFrame,
    period: int | list[int],
    price_column: str = "close",
) -> pd.Series | pd.DataFrame:
    ...
```

Registered in `FeatureService` as:

```python
_INDICATOR_REGISTRY = {
    "ema": lambda df, params: compute_ema_from_ohlcv(
        df, int(params["period"]), price_column=params.get("price_column", "close")
    ),
    ...
}
```

### Strategy YAML reference

```yaml
indicators:
  - id: fast_ema
    type: ema
    params:
      period: 12
```

`type` maps to registry key; `id` is the alias used in rule expressions.

---

## Future (Package 05)

Indicators will implement the full `Plugin` contract from [AES-0202](../architecture/AES-0202-Plugin-Architecture.md) and register via `PluginRegistry`. Until then, `_INDICATOR_REGISTRY` is the authoritative runtime registry.

---

## Related Documents

| Document | Purpose |
|----------|---------|
| [REQ-IND-EMA-001](../requirements/REQ-IND-EMA-001.md) | EMA requirement |
| [REQ-IND-SMA-001](../requirements/REQ-IND-SMA-001.md) | SMA requirement |
| [REQ-FEAT-STORE-001](../requirements/REQ-FEAT-STORE-001.md) | Feature store |

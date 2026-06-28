# Performance benchmarks — Rev 2

Targets validated by `tests/benchmarks/test_performance.py` (marker `@pytest.mark.benchmark`).

| Target | Threshold | Test |
|--------|-----------|------|
| Indicator generation (EMA, 252 bars) | &lt; 2s | `test_indicator_generation_under_2s` |
| Backtest (5 symbols, 120 bars) | &lt; 15s | `test_backtest_small_universe_reasonable_time` |

## Running locally

```bash
cd athena/athena-core
pytest -m benchmark -v
```

## CI

Benchmarks run in a separate non-blocking CI job (`benchmark` in `.github/workflows/ci.yml`).

Default `pytest` excludes benchmarks via `addopts = "-m 'not integration and not benchmark'"`.

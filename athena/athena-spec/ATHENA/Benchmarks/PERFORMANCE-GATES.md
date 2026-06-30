# Performance Gates

> **Enforced in:** `athena-testing/benchmarks/`  
> **CI:** Optional `pytest -m benchmark` (excluded from default CI per athena-core config)

## Gate Definitions

| Gate ID | APS | Metric | Threshold | Test |
|---------|-----|--------|-----------|------|
| PG-IND-100K | APS-IND-BENCH-100K-001 | 100k-row rolling mean | < 2.0s | `test_indicator_throughput.py` |
| PG-EVT-PUB | APS-004 | 10k event publish | < 0.5s | deferred |
| PG-BOOT | APS-001 | Core bootstrap | < 1.0s | deferred |

## Running Gates

```bash
cd athena-testing
pytest benchmarks/ -m benchmark
```

## Adding Gates

1. Add row to this table.
2. Implement stub in `athena-testing/benchmarks/`.
3. Link **Benchmarks** field in APS traceability block.

## Failure Policy

- **CI default:** gates are informational (benchmark marker excluded).
- **Release:** PG-IND-100K must pass before REL sign-off.

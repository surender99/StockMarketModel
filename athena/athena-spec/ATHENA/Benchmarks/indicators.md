# Indicator Benchmarks — Phase 3

Performance targets for Release-04 / PHASE-3 Indicators APS.

| Target | APS / REQ | Evidence |
|--------|-----------|----------|
| EMA 10k bars < 50 ms | APS-IND-EMA-001 | `tests/test_indicator_aps.py` |
| IndicatorEngine single compute 10k bars < 100 ms | APS-IND-ENGINE-001 | `tests/test_indicator_framework.py` |
| `compute_many` 3 indicators 10k bars < 200 ms | APS-IND-COMPOSE-001 | `tests/test_indicator_framework.py` |
| Output validation < 1 ms | APS-IND-VALIDATE-001 | `tests/test_indicator_framework.py` |

**Golden fixtures:** [Golden-Datasets/ohlcv-sample-30d.csv](../Golden-Datasets/ohlcv-sample-30d.csv)

**Code benchmarks:** [athena-core/benchmarks/](../../../athena-core/benchmarks/README.md)

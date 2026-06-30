# Pattern Benchmarks — Phase 4

Performance targets for Release-05 / PHASE-4 Patterns APS.

| Target | APS / REQ | Evidence |
|--------|-----------|----------|
| Single candlestick detect 1k bars < 20 ms | APS-PAT-CANDLE-001 | `tests/test_pattern_recognition_framework.py` |
| Chart pattern detect 1k bars < 50 ms | APS-PAT-CHART-001 | `tests/test_pattern_recognition_framework.py` |
| Pattern registry resolve < 1 ms | APS-PAT-REGISTRY-001 | `tests/test_pattern_aps.py` |

**Golden fixtures:** [Golden-Datasets/ohlcv-sample-30d.csv](../Golden-Datasets/ohlcv-sample-30d.csv)

**Code benchmarks:** [athena-core/benchmarks/](../../../athena-core/benchmarks/README.md)

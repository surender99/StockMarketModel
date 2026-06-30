# Indicator Benchmarks — Phase 3 (Expanded Architecture)

Performance targets from `References/PHASE 3 Architecture.docx`.

| Target | APS / REQ | Evidence |
|--------|-----------|----------|
| EMA 10k bars < 50 ms | APS-IND-EMA-001 / APS-IND-BENCH-10K-001 | `tests/test_indicator_aps.py` |
| IndicatorEngine single compute 10k bars < 100 ms | APS-IND-ENGINE-001 | `tests/test_indicator_framework.py` |
| `compute_many` 3 indicators 10k bars < 200 ms | APS-IND-COMPOSE-001 | `tests/test_indicator_framework.py` |
| Pipeline 2-stage 200 bars | APS-IND-PIPELINE-001 | `tests/test_indicator_architecture.py` |
| Price transform 100 bars vectorized | APS-PRICE-HLC3-001 | `tests/test_indicator_architecture.py` |
| Output validation < 1 ms | APS-IND-VALIDATE-001 | `tests/test_indicator_framework.py` |

## Deferred scale targets (APS-IND-BENCH-*)

| Scale | APS | Status |
|-------|-----|--------|
| 100K candles | APS-IND-BENCH-100K-001 | Deferred |
| 1M candles | APS-IND-BENCH-1M-001 | Deferred |
| Streaming throughput | APS-IND-BENCH-STREAM-001 | Deferred |
| GPU engine | APS-IND-BENCH-GPU-001 | Deferred |

**Golden fixtures:** [Golden-Datasets/ohlcv-sample-30d.csv](../Golden-Datasets/ohlcv-sample-30d.csv)

**Code benchmarks:** [athena-core/benchmarks/](../../../athena-core/benchmarks/README.md)

**Cross-library validation tolerance:** 1e-8 (APS-VALIDATE-IND-001)

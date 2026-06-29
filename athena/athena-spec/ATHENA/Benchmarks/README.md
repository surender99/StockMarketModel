# Benchmarks

Performance targets and benchmark test references. Domain benchmarks remain at legacy paths.

## Foundation (APS-001–015)

| Target | Source | Test ref |
|--------|--------|----------|
| 100 KB config load < 20 ms | APS-001, APS-014 | `tests/test_core_framework.py` |
| Config reload < 10 ms | APS-001 | Manual / future benchmark |
| Feature cache hit < 5 ms | APS-009 | `tests/test_feature_store.py` |
| EMA 10k bars < 50 ms | REQ-IND-EMA-001 | `tests/test_indicators_ema.py` |

## Domain Benchmarks

| Domain | Path |
|--------|------|
| Feature engineering | [feature-engineering/benchmarks/](../../feature-engineering/benchmarks/performance.md) |
| Backtesting | [backtesting/benchmarks/](../../backtesting/benchmarks/performance.md) |
| Strategy | [strategy-engine/benchmarks/](../../strategy-engine/benchmarks/performance.md) |
| Portfolio | [portfolio-engine/benchmarks/](../../portfolio-engine/benchmarks/performance.md) |
| Statistics | [statistics/benchmarks/](../../statistics/benchmarks/performance.md) |
| Patterns | [pattern-recognition/benchmarks/](../../pattern-recognition/benchmarks/performance.md) |
| Research | [research-engine/benchmarks/](../../research-engine/benchmarks/performance.md) |
| ML | [machine-learning/benchmarks/](../../machine-learning/benchmarks/performance.md) |
| Market intelligence | [market-intelligence/benchmarks/](../../market-intelligence/benchmarks/targets.md) |
| AI research | [ai-research/benchmarks/](../../ai-research/benchmarks/quality.md) |

**Code benchmarks:** [athena-core/benchmarks/](../../../athena-core/benchmarks/README.md)

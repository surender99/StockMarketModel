# Strategy Benchmarks — Phase 5

Performance targets for Release-06 / PHASE-5 Strategies APS.

| Target | APS / REQ | Evidence |
|--------|-----------|----------|
| Strategy config validation < 5 ms | APS-STRAT-VALIDATE-001 | `tests/test_strategy_engine_framework.py` |
| Signal engine single bar < 10 ms | APS-STRAT-SIGNAL-001 | `tests/test_strategy_engine_framework.py` |
| Expression evaluate < 1 ms | APS-STRAT-EXPR-001 | `tests/test_strategy_expression.py` |
| Strategy registry resolve < 1 ms | APS-STRAT-REGISTRY-001 | `tests/test_strategy_aps.py` |

**Golden fixtures:** [Golden-Datasets/ohlcv-sample-30d.csv](../Golden-Datasets/ohlcv-sample-30d.csv)

**Code benchmarks:** [athena-core/benchmarks/](../../../athena-core/benchmarks/README.md)

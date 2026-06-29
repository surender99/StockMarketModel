# Data Platform Benchmarks — Phase 2

Performance targets for Release-02 / PHASE-2 Data Platform APS.

| Target | APS / REQ | Evidence |
|--------|-----------|----------|
| Single-symbol yfinance ingest (30 bars) < 5 s | APS-IMPORT-YAHOO-001 | Manual / integration (network) |
| OHLCV quality check 10k rows < 50 ms | APS-VALIDATE-OHLC-001, APS-DQ-SCORE-001 | `tests/test_data_platform.py` |
| `clean_ohlcv_frame` 10k rows < 30 ms | APS-CLEAN-001 | `tests/test_data_platform.py` |
| Parquet read 1 symbol 5y daily < 100 ms | APS-STORAGE-PARQUET-001 | `athena-core/benchmarks/` (future) |
| Feature store lookup cache hit < 5 ms | APS-FS-CACHE-001 | `tests/test_feature_store.py` |
| Config bootstrap data platform < 50 ms | APS-DATA-HIST-001 | `tests/test_data_platform.py` |

**Golden fixtures:** [Golden-Datasets/](../Golden-Datasets/ohlcv-sample-30d.csv), [ohlcv-dirty-sample.csv](../Golden-Datasets/ohlcv-dirty-sample.csv)

**Code benchmarks:** [athena-core/benchmarks/](../../../athena-core/benchmarks/README.md)

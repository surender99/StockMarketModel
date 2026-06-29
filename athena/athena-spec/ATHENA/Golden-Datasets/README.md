# Golden Datasets

Small, version-controlled fixtures for reproducible tests and APS validation. Not production data.

| File | Purpose | Used by |
|------|---------|---------|
| [ohlcv-sample-30d.csv](ohlcv-sample-30d.csv) | 30 business days OHLCV for TEST.NS | Feature store, indicator tests |
| [symbols-sample.csv](symbols-sample.csv) | 5 NSE symbols | Ingest/scanner examples |
| [config-minimal.yaml](config-minimal.yaml) | Minimal Athena config | Bootstrap smoke tests |

**Larger examples:** [athena-examples/](../../../athena-examples/) (`nifty500_sample.csv`, strategy YAML).

**Test fixtures:** inline fixtures in `athena-core/tests/` mirror these datasets for pytest.

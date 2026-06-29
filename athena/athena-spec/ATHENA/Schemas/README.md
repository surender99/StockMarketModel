# Schemas

JSON and YAML schema index. Canonical files remain at legacy paths.

## Core Schemas

| Schema | Path | Used by |
|--------|------|---------|
| OHLCV | [schemas/ohlcv-schema.json](../../schemas/ohlcv-schema.json) | Ingest, feature store |
| Dataset metadata | [dataset-metadata.json](dataset-metadata.json) | Dataset registry — APS-DATASET-001 |
| Backtest config | [backtesting/schemas/backtest-config.json](../../backtesting/schemas/backtest-config.json) | Backtest engine |
| Indicator config | [feature-engineering/schemas/indicator-config.json](../../feature-engineering/schemas/indicator-config.json) | Feature pipeline |
| Pattern event | [pattern-recognition/schemas/pattern-event.json](../../pattern-recognition/schemas/pattern-event.json) | Pattern engine |
| Portfolio config | [portfolio-engine/schemas/portfolio-config.json](../../portfolio-engine/schemas/portfolio-config.json) | Portfolio engine |
| Statistics report | [statistics/schemas/statistics-report.json](../../statistics/schemas/statistics-report.json) | Statistics engine |
| Experiment | [research-engine/schemas/experiment-schema.json](../../research-engine/schemas/experiment-schema.json) | Research engine |
| Model metadata | [machine-learning/schemas/model-metadata.json](../../machine-learning/schemas/model-metadata.json) | ML platform |

**Validation:** Pydantic models in `athena-core` are the runtime source of truth; JSON schemas document interchange formats.

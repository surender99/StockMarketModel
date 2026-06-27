# ADR-0001 – pandas + Parquet for MVP Data Layer

> **Status:** Accepted  
> **Date:** 2026-06-27  
> **Deciders:** Athena platform architects

## Context

Athena's MVP targets NSE daily OHLCV research on a single workstation. The data layer must support ingest, feature materialization, and backtest reads with minimal operational overhead. Team familiarity, ecosystem maturity, and time-to-MVP are primary constraints.

## Decision

Use **pandas** as the in-memory tabular API and **Parquet** (via pyarrow) as the on-disk feature-store format for the MVP.

## Alternatives Considered

| Option | Pros | Cons |
|--------|------|------|
| **pandas + Parquet** (chosen) | Broad team familiarity; rich quant ecosystem; pyarrow compression; trivial yfinance → DataFrame path | Not the fastest for very large scans; single-threaded pandas hotspots |
| **Polars** | Faster lazy evaluation; better memory on wide frames | New API surface; fewer examples in quant community; migration cost from pandas-centric indicators |
| **DuckDB** | Excellent analytical SQL over Parquet; fast aggregations | Extra query layer; less natural fit for row-wise indicator pipelines in MVP |
| **Polars + DuckDB hybrid** | Best long-term analytics performance | Over-engineered for Phase 0–7 scope; delays MVP delivery |

## Consequences

- **Positive:** Fastest path from yfinance ingest to backtest; Parquet files are portable and diff-friendly for small universes; aligns with scikit-learn / SHAP stacks already in use.
- **Negative:** Full NIFTY 500 universe scans may need batching or a future columnar migration; no built-in query planner for ad-hoc SQL analytics.
- **Neutral:** ADR does not forbid adding Polars or DuckDB adapters behind `DataProvider` ports in a later phase.

## Compliance

- [x] [ATH-003 Repository Architecture](../ATH-003-Repository-Architecture.md) layers respected
- [x] [AES-0005 Quant Standards](../governance/AES-0005-Quant-Standards.md) (if research-impacting)
- [ ] Related REQ or RFC linked below

## References

- REQ-DATA-INGEST-001, REQ-FEAT-STORE-001
- `athena-core` Parquet feature store and `yfinance_client.py`

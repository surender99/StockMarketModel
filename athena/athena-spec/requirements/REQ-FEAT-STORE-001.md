# REQ-FEAT-STORE-001

**Requirement ID:** REQ-FEAT-STORE-001

**Title:** Feature Store

**Purpose:** Persist computed indicator and feature values so they are never recomputed when already available for a given symbol, feature name, parameters, and dataset version.

**Description:** The feature store provides get/put semantics keyed by `(symbol, feature_id, params_hash, data_version)`. Features are stored as Parquet (or partitioned dataset) with metadata describing provenance (source REQ, computation timestamp, input data hash). Consumers query by symbol and date range.

**Inputs:**
- Feature identity: `feature_id` (e.g. `ema`), `params` (e.g. `{period: 21}`)
- Symbol, date range
- Feature values (Series or DataFrame) on write

**Outputs:**
- On read: DataFrame/Series aligned to requested dates, or cache miss indicator
- On write: confirmation + storage path

**Configuration:**
```yaml
feature_store:
  base_path: ./data/features
  partition_by: [symbol, feature_id]
  compression: snappy
  data_version: "v1"  # bump when OHLCV schema or source changes
```

**Algorithm:**
1. Compute `params_hash = sha256(json.dumps(params, sort_keys=True))[:16]`.
2. Resolve path: `{base_path}/{symbol}/{feature_id}/{params_hash}/`.
3. **Get:** if Parquet exists and `data_version` matches, read and slice date range; else return miss.
4. **Put:** write Parquet with metadata sidecar JSON (feature_id, params, data_version, created_at, row_count).
5. Never overwrite different `data_version` without explicit purge flag.

**Dependencies:**
- pyarrow, pandas
- REQ-DATA-INGEST-001 (data_version tied to OHLCV ingest)

**Acceptance Criteria:**
- [ ] Cache hit skips indicator recomputation (verified via mock/spy)
- [ ] Different params produce separate storage paths
- [ ] Date range query returns only requested rows
- [ ] Metadata sidecar includes feature_id, params, data_version, timestamp
- [ ] `data_version` mismatch triggers recompute path

**Performance Target:**
- Read 5 years daily features for one symbol: < 100 ms
- Write same: < 200 ms

**Unit Tests:**
- Put then get round-trip
- Params hash isolation
- Version mismatch behavior
- Missing cache returns explicit miss (not exception)

**Integration Tests:**
- EMA computed once, stored, retrieved identically on second call

**Future Enhancements:**
- DuckDB query layer
- Remote store (S3)
- Feature lineage graph
- TTL / garbage collection for stale versions

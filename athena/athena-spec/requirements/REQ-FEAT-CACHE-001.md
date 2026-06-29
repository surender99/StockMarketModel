# REQ-FEAT-CACHE-001

**Requirement ID:** REQ-FEAT-CACHE-001

**Title:** Feature Cache Policies

**Purpose:** Control how `FeatureService` interacts with the Parquet feature store on read.

**Description:** `FeatureCachePolicy` enum on `FeatureStoreConfig`:
- `compute_on_miss` (default): read cache; compute and persist on miss
- `cache_only`: return cached data only; raise on miss
- `force_recompute`: skip cache read; always compute and persist

**Acceptance Criteria:**
- [ ] Default policy preserves existing compute-on-miss behavior
- [ ] `force_recompute` increments compute count even when cache exists
- [ ] `cache_only` raises `ValueError` on cache miss

**Unit Tests:** `tests/test_feature_engineering_framework.py`

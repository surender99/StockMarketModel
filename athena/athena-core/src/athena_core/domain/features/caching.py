"""Feature cache policies — REQ-FEAT-CACHE-001, ATH-REL-003 §10."""

from __future__ import annotations

from enum import StrEnum


class FeatureCachePolicy(StrEnum):
    """Controls how FeatureService resolves cache hits and misses."""

    COMPUTE_ON_MISS = "compute_on_miss"
    CACHE_ONLY = "cache_only"
    FORCE_RECOMPUTE = "force_recompute"

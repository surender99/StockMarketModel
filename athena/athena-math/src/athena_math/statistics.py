"""Statistics — re-export from athena-core domain statistics."""

from __future__ import annotations

from athena_core.domain.statistics.correlation import correlation_matrix as compute_correlation_matrix

__all__ = ["compute_correlation_matrix"]

"""Experiment result repository — ATH-REL-010 §5.5, REQ-RS-RESULTS-001."""

from __future__ import annotations

from typing import Any

from athena_core.application.experiment_tracker import ExperimentRecord, ExperimentTracker


class ResultRepository:
    """Rank and compare experiment results — FR-007, FR-008."""

    def __init__(self, tracker: ExperimentTracker) -> None:
        self._tracker = tracker

    def history(self, limit: int = 50) -> list[ExperimentRecord]:
        """Return experiment history."""
        return self._tracker.list_records(limit=limit)

    def compare(
        self,
        *,
        experiment_ids: list[str] | None = None,
        latest: int | None = None,
        metric_keys: list[str] | None = None,
    ) -> dict[str, Any]:
        """Side-by-side experiment comparison."""
        return self._tracker.compare_experiments(
            experiment_ids,
            latest=latest,
            metric_keys=metric_keys,
        )

    def rank(
        self,
        metric_key: str,
        *,
        limit: int = 10,
        descending: bool = True,
    ) -> list[dict[str, Any]]:
        """Rank experiments by a metric — FR-008."""
        records = self._tracker.list_records(limit=200)
        scored: list[tuple[float, ExperimentRecord]] = []
        for record in records:
            value = record.metrics.get(metric_key)
            if isinstance(value, (int, float)):
                scored.append((float(value), record))
        scored.sort(key=lambda item: item[0], reverse=descending)
        return [
            {
                "rank": idx + 1,
                "experiment_id": record.experiment_id,
                "strategy_id": record.strategy_id,
                metric_key: value,
            }
            for idx, (value, record) in enumerate(scored[:limit])
        ]

"""Review manager — ATH-REL-016."""

from __future__ import annotations

from athena_core.domain.review import (
    GateStatus,
    ReleaseGate,
    ReviewResult,
    ReviewType,
    evaluate_release_gate,
    run_review,
)


class ReviewManager:
    """Orchestrate engineering reviews and release gates."""

    def run_all_reviews(self, passed: dict[ReviewType, list[str]]) -> ReleaseGate:
        results = [
            run_review(rt, passed_items=passed.get(rt, []))
            for rt in ReviewType
        ]
        return evaluate_release_gate("release", results)

    def gate_status(self, gate: ReleaseGate) -> GateStatus:
        return gate.status

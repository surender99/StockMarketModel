"""Engineering review framework — ATH-REL-016."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any


class ReviewType(StrEnum):
    ARCHITECTURE = "architecture"
    CODE = "code"
    QUANT = "quantitative"
    STATISTICAL = "statistical"
    SECURITY = "security"
    PERFORMANCE = "performance"
    AI = "ai"


class GateStatus(StrEnum):
    PASSED = "passed"
    FAILED = "failed"
    WAIVED = "waived"


@dataclass
class ReviewChecklist:
    review_type: ReviewType
    items: list[str]
    required: bool = True


@dataclass
class ReviewResult:
    review_type: ReviewType
    passed: bool
    findings: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class ReleaseGate:
    release_id: str
    checks: list[ReviewResult] = field(default_factory=list)

    @property
    def status(self) -> GateStatus:
        required_failed = any(not c.passed for c in self.checks)
        return GateStatus.FAILED if required_failed else GateStatus.PASSED


REVIEW_CHECKLISTS: dict[ReviewType, ReviewChecklist] = {
    ReviewType.ARCHITECTURE: ReviewChecklist(
        ReviewType.ARCHITECTURE,
        ["Clean architecture layers respected", "No circular dependencies"],
    ),
    ReviewType.CODE: ReviewChecklist(
        ReviewType.CODE, ["Tests pass", "Lint clean", "REQ traceability"]
    ),
    ReviewType.QUANT: ReviewChecklist(
        ReviewType.QUANT, ["Backtest validated", "Walk-forward performed"]
    ),
    ReviewType.STATISTICAL: ReviewChecklist(
        ReviewType.STATISTICAL, ["Hypothesis tests documented"]
    ),
    ReviewType.SECURITY: ReviewChecklist(
        ReviewType.SECURITY, ["Secrets not committed", "Auth configured"]
    ),
    ReviewType.PERFORMANCE: ReviewChecklist(
        ReviewType.PERFORMANCE, ["Benchmarks within targets"]
    ),
    ReviewType.AI: ReviewChecklist(
        ReviewType.AI, ["AI outputs cite experiment IDs"]
    ),
}


def run_review(review_type: ReviewType, *, passed_items: list[str]) -> ReviewResult:
    checklist = REVIEW_CHECKLISTS[review_type]
    missing = [item for item in checklist.items if item not in passed_items]
    return ReviewResult(
        review_type=review_type,
        passed=len(missing) == 0,
        findings=missing,
    )


def evaluate_release_gate(release_id: str, results: list[ReviewResult]) -> ReleaseGate:
    return ReleaseGate(release_id=release_id, checks=results)

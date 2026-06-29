"""Engineering review framework tests — ATH-REL-016."""

from __future__ import annotations

from athena_core.application.review_manager import ReviewManager
from athena_core.domain.review import GateStatus, ReviewType, run_review


def test_req_rev_gate_001_release_gate() -> None:
    """REQ-REV-GATE-001 — release gates."""
    mgr = ReviewManager()
    passed = {rt: [] for rt in ReviewType}
    gate = mgr.run_all_reviews(passed)
    assert gate.status == GateStatus.FAILED


def test_req_rev_arch_001_architecture_review() -> None:
    """REQ-REV-ARCH-001 — architecture reviews."""
    result = run_review(
        ReviewType.ARCHITECTURE,
        passed_items=["Clean architecture layers respected", "No circular dependencies"],
    )
    assert result.passed


def test_req_rev_code_001_code_review() -> None:
    """REQ-REV-CODE-001 — code reviews."""
    result = run_review(ReviewType.CODE, passed_items=["Tests pass"])
    assert not result.passed


def test_req_rev_quant_001_quant_review() -> None:
    """REQ-REV-QUANT-001 — quantitative reviews."""
    result = run_review(
        ReviewType.QUANT,
        passed_items=["Backtest validated", "Walk-forward performed"],
    )
    assert result.passed

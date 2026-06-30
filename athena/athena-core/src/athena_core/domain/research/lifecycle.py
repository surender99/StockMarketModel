"""Experiment lifecycle states — ATH-REL-010 §5.2, AES-1001."""

from __future__ import annotations

from enum import Enum


class ExperimentState(str, Enum):
    """Experiment lifecycle — AES-1001, APS-EXP-LIFECYCLE-001."""

    DRAFT = "draft"
    CONFIGURED = "configured"
    RUNNING = "running"
    COMPLETED = "completed"
    VALIDATED = "validated"
    REJECTED = "rejected"
    ARCHIVED = "archived"


VALID_TRANSITIONS: dict[ExperimentState, frozenset[ExperimentState]] = {
    ExperimentState.DRAFT: frozenset(
        {ExperimentState.CONFIGURED, ExperimentState.RUNNING, ExperimentState.ARCHIVED}
    ),
    ExperimentState.CONFIGURED: frozenset({ExperimentState.RUNNING, ExperimentState.ARCHIVED}),
    ExperimentState.RUNNING: frozenset(
        {ExperimentState.COMPLETED, ExperimentState.REJECTED, ExperimentState.ARCHIVED}
    ),
    ExperimentState.COMPLETED: frozenset(
        {ExperimentState.VALIDATED, ExperimentState.REJECTED, ExperimentState.ARCHIVED}
    ),
    ExperimentState.VALIDATED: frozenset({ExperimentState.ARCHIVED}),
    ExperimentState.REJECTED: frozenset({ExperimentState.ARCHIVED, ExperimentState.DRAFT}),
    ExperimentState.ARCHIVED: frozenset(),
}


def can_transition(current: ExperimentState, target: ExperimentState) -> bool:
    """Return True when lifecycle transition is allowed."""
    return target in VALID_TRANSITIONS.get(current, frozenset())


def transition(current: ExperimentState, target: ExperimentState) -> ExperimentState:
    """Apply lifecycle transition or raise ValueError."""
    if not can_transition(current, target):
        msg = f"invalid transition: {current.value} -> {target.value}"
        raise ValueError(msg)
    return target

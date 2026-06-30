"""Workflow engine — APS-006."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

StepFn = Callable[[dict[str, Any]], dict[str, Any]]


class WorkflowStatus(StrEnum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class WorkflowStep:
    name: str
    execute: StepFn


@dataclass
class WorkflowResult:
    status: WorkflowStatus
    context: dict[str, Any] = field(default_factory=dict)
    error: str | None = None


class WorkflowEngine:
    """Sequential workflow orchestrator with shared context."""

    def __init__(self) -> None:
        self._workflows: dict[str, list[WorkflowStep]] = {}

    def define(self, workflow_id: str, steps: list[WorkflowStep]) -> None:
        self._workflows[workflow_id] = steps

    def run(self, workflow_id: str, initial_context: dict[str, Any] | None = None) -> WorkflowResult:
        steps = self._workflows.get(workflow_id)
        if steps is None:
            return WorkflowResult(WorkflowStatus.FAILED, error=f"unknown workflow: {workflow_id}")
        context = dict(initial_context or {})
        for step in steps:
            try:
                context = step.execute(context)
            except Exception as exc:  # noqa: BLE001
                return WorkflowResult(WorkflowStatus.FAILED, context=context, error=str(exc))
        return WorkflowResult(WorkflowStatus.COMPLETED, context=context)

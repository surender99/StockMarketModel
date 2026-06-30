"""Research hypothesis management — PHASE 9 QREP, APS-HYPOTHESIS-*."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum


class HypothesisStatus(str, Enum):
    """Hypothesis validation state — APS-HYPOTHESIS-TRACKING-001."""

    PENDING = "pending"
    VALIDATED = "validated"
    REJECTED = "rejected"


@dataclass
class Hypothesis:
    """Research hypothesis — APS-HYPOTHESIS-CORE-001."""

    hypothesis_id: str
    project_id: str
    statement: str
    objective: str = ""
    expected_outcome: str = ""
    success_criteria: str = ""
    status: HypothesisStatus = HypothesisStatus.PENDING
    linked_experiments: list[str] = field(default_factory=list)
    linked_strategies: list[str] = field(default_factory=list)
    linked_datasets: list[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        project_id: str,
        statement: str,
        *,
        objective: str = "",
        expected_outcome: str = "",
        success_criteria: str = "",
    ) -> Hypothesis:
        return cls(
            hypothesis_id=str(uuid.uuid4()),
            project_id=project_id,
            statement=statement,
            objective=objective,
            expected_outcome=expected_outcome,
            success_criteria=success_criteria,
        )

    def link_experiment(self, experiment_id: str) -> None:
        if experiment_id not in self.linked_experiments:
            self.linked_experiments.append(experiment_id)
            self.updated_at = datetime.now(UTC)

    def link_strategy(self, strategy_id: str) -> None:
        if strategy_id not in self.linked_strategies:
            self.linked_strategies.append(strategy_id)
            self.updated_at = datetime.now(UTC)

    def link_dataset(self, dataset_id: str) -> None:
        if dataset_id not in self.linked_datasets:
            self.linked_datasets.append(dataset_id)
            self.updated_at = datetime.now(UTC)

    def validate(self) -> None:
        self.status = HypothesisStatus.VALIDATED
        self.updated_at = datetime.now(UTC)

    def reject(self) -> None:
        self.status = HypothesisStatus.REJECTED
        self.updated_at = datetime.now(UTC)


class HypothesisRegistry:
    """In-memory hypothesis store — APS-HYPOTHESIS-LINKS-001."""

    def __init__(self) -> None:
        self._hypotheses: dict[str, Hypothesis] = {}

    def register(self, hypothesis: Hypothesis) -> Hypothesis:
        self._hypotheses[hypothesis.hypothesis_id] = hypothesis
        return hypothesis

    def get(self, hypothesis_id: str) -> Hypothesis:
        if hypothesis_id not in self._hypotheses:
            raise KeyError(f"hypothesis not found: {hypothesis_id}")
        return self._hypotheses[hypothesis_id]

    def list_by_project(self, project_id: str) -> list[Hypothesis]:
        return [h for h in self._hypotheses.values() if h.project_id == project_id]

    def list_by_status(self, status: HypothesisStatus) -> list[Hypothesis]:
        return [h for h in self._hypotheses.values() if h.status == status]

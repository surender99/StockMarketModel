"""Research workspace context — ATH-REL-010 §5.1."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

from athena_core.domain.research.lifecycle import ExperimentState


@dataclass
class ResearchProject:
    """Research workspace project — FR-001."""

    project_id: str
    name: str
    description: str = ""
    template: str = "default"
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(cls, name: str, *, description: str = "", template: str = "default") -> ResearchProject:
        return cls(project_id=str(uuid.uuid4()), name=name, description=description, template=template)


@dataclass
class ExperimentSpec:
    """Experiment definition within a research project — FR-002."""

    experiment_id: str
    project_id: str
    name: str
    state: ExperimentState = ExperimentState.DRAFT
    version: int = 1
    dataset_version: str = ""
    dependencies: list[str] = field(default_factory=list)
    params: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        project_id: str,
        name: str,
        *,
        dataset_version: str = "",
        dependencies: list[str] | None = None,
        params: dict[str, Any] | None = None,
    ) -> ExperimentSpec:
        return cls(
            experiment_id=str(uuid.uuid4()),
            project_id=project_id,
            name=name,
            dataset_version=dataset_version,
            dependencies=list(dependencies or []),
            params=dict(params or {}),
        )

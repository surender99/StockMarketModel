"""Research workspace manager — ATH-REL-010 §5.1, REQ-RS-WORKSPACE-001."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from athena_core.application.experiment_tracker import ExperimentTracker
from athena_core.application.research_pipeline import PipelineRunResult, ResearchPipeline
from athena_core.application.result_repository import ResultRepository
from athena_core.domain.research.context import ExperimentSpec, ResearchProject
from athena_core.domain.research.dataset import DatasetSnapshot
from athena_core.domain.research.knowledge import KnowledgeEntry
from athena_core.domain.research.lifecycle import ExperimentState, transition


class ResearchManager:
    """Orchestrate research workspace workflows — FR-001, FR-012."""

    def __init__(
        self,
        *,
        pipeline: ResearchPipeline | None = None,
        tracker: ExperimentTracker | None = None,
    ) -> None:
        self._pipeline = pipeline or ResearchPipeline()
        self._tracker = tracker
        self._projects: dict[str, ResearchProject] = {}
        self._experiments: dict[str, ExperimentSpec] = {}
        self._snapshots: dict[str, DatasetSnapshot] = {}
        self._knowledge: dict[str, KnowledgeEntry] = {}

    @property
    def result_repository(self) -> ResultRepository | None:
        if self._tracker is None:
            return None
        return ResultRepository(self._tracker)

    def create_project(self, name: str, *, description: str = "", template: str = "default") -> ResearchProject:
        """Create research project — FR-001."""
        project = ResearchProject.create(name, description=description, template=template)
        self._projects[project.project_id] = project
        return project

    def get_project(self, project_id: str) -> ResearchProject:
        if project_id not in self._projects:
            raise KeyError(f"project not found: {project_id}")
        return self._projects[project_id]

    def list_projects(self) -> list[ResearchProject]:
        return sorted(self._projects.values(), key=lambda p: p.created_at, reverse=True)

    def create_experiment(
        self,
        project_id: str,
        name: str,
        *,
        dataset_version: str = "",
        dependencies: list[str] | None = None,
        params: dict[str, Any] | None = None,
    ) -> ExperimentSpec:
        """Create experiment in project — FR-002."""
        self.get_project(project_id)
        spec = ExperimentSpec.create(
            project_id,
            name,
            dataset_version=dataset_version,
            dependencies=dependencies,
            params=params,
        )
        self._experiments[spec.experiment_id] = spec
        return spec

    def advance_experiment(self, experiment_id: str, target: ExperimentState) -> ExperimentSpec:
        """Transition experiment lifecycle — FR-003."""
        spec = self._experiments[experiment_id]
        spec.state = transition(spec.state, target)
        spec.updated_at = datetime.now(UTC)
        if target in (ExperimentState.COMPLETED, ExperimentState.VALIDATED):
            spec.version += 1
        return spec

    def capture_dataset(
        self,
        dataset_id: str,
        version: str,
        payload: dict[str, Any],
        *,
        parent_snapshot_id: str | None = None,
    ) -> DatasetSnapshot:
        """Capture dataset snapshot — FR-004."""
        snapshot = DatasetSnapshot.capture(
            dataset_id,
            version,
            payload,
            parent_snapshot_id=parent_snapshot_id,
        )
        self._snapshots[snapshot.snapshot_id] = snapshot
        return snapshot

    def add_knowledge(
        self,
        project_id: str,
        title: str,
        body: str,
        *,
        tags: list[str] | None = None,
        references: list[str] | None = None,
    ) -> KnowledgeEntry:
        """Add knowledge base entry — FR-011."""
        self.get_project(project_id)
        entry = KnowledgeEntry.create(project_id, title, body, tags=tags, references=references)
        self._knowledge[entry.entry_id] = entry
        return entry

    def list_knowledge(self, project_id: str) -> list[KnowledgeEntry]:
        return [e for e in self._knowledge.values() if e.project_id == project_id]

    def run_pipeline(
        self,
        experiment_id: str,
        *,
        context: dict[str, Any] | None = None,
        stages: list[str] | None = None,
    ) -> PipelineRunResult:
        """Execute research pipeline for experiment — FR-006."""
        spec = self._experiments[experiment_id]
        if spec.state == ExperimentState.DRAFT:
            self.advance_experiment(experiment_id, ExperimentState.RUNNING)
        result = self._pipeline.run(spec, context=context, stages=stages)
        if result.success and spec.state == ExperimentState.RUNNING:
            self.advance_experiment(experiment_id, ExperimentState.COMPLETED)
        elif not result.success and spec.state == ExperimentState.RUNNING:
            self.advance_experiment(experiment_id, ExperimentState.REJECTED)
        return result

"""Research domain models — AES-1000, ATH-REL-010, PHASE 9 QREP."""

from athena_core.domain.research.catalog import (
    QREP_CATALOG,
    QrepCatalogEntry,
    get_qrep_entry,
    list_mvp_qrep,
)
from athena_core.domain.research.context import ExperimentSpec, ResearchProject
from athena_core.domain.research.dataset import DatasetSnapshot, compare_snapshots, reproducibility_hash
from athena_core.domain.research.events import ResearchEvent, ResearchEventBus, ResearchEventType
from athena_core.domain.research.hypothesis import (
    Hypothesis,
    HypothesisRegistry,
    HypothesisStatus,
)
from athena_core.domain.research.knowledge import KnowledgeEntry
from athena_core.domain.research.lifecycle import ExperimentState, can_transition, transition
from athena_core.domain.research.reproducibility import (
    ReproducibilityBundle,
    bundle_hash,
    replay_experiment_bundle,
    verify_reproducibility,
)
from athena_core.domain.research.research_plugins import (
    list_pipeline_stages,
    register_builtin_research_plugins,
)

__all__ = [
    "DatasetSnapshot",
    "ExperimentSpec",
    "ExperimentState",
    "Hypothesis",
    "HypothesisRegistry",
    "HypothesisStatus",
    "KnowledgeEntry",
    "QREP_CATALOG",
    "QrepCatalogEntry",
    "ResearchEvent",
    "ResearchEventBus",
    "ResearchEventType",
    "ResearchProject",
    "ReproducibilityBundle",
    "bundle_hash",
    "can_transition",
    "compare_snapshots",
    "get_qrep_entry",
    "list_mvp_qrep",
    "list_pipeline_stages",
    "register_builtin_research_plugins",
    "replay_experiment_bundle",
    "reproducibility_hash",
    "transition",
    "verify_reproducibility",
]

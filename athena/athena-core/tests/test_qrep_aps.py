"""PHASE 9 QREP APS catalog and domain tests."""

from __future__ import annotations

from datetime import UTC, datetime

from athena_core.application.research_manager import ResearchManager
from athena_core.domain.research import (
    ExperimentState,
    Hypothesis,
    HypothesisRegistry,
    HypothesisStatus,
    QREP_CATALOG,
    ReproducibilityBundle,
    ResearchEvent,
    ResearchEventBus,
    ResearchEventType,
    bundle_hash,
    can_transition,
    list_mvp_qrep,
    replay_experiment_bundle,
    transition,
    verify_reproducibility,
)
from athena_core.domain.research.context import ExperimentSpec
from athena_core.domain.research.knowledge import KnowledgeEntry


def test_qrep_catalog_mvp_entries() -> None:
    mvp = list_mvp_qrep()
    assert len(mvp) >= 10
    assert len(QREP_CATALOG) >= 18


def test_aps_exp_lifecycle_configured_state() -> None:
    assert can_transition(ExperimentState.DRAFT, ExperimentState.CONFIGURED)
    assert can_transition(ExperimentState.CONFIGURED, ExperimentState.RUNNING)
    assert transition(ExperimentState.DRAFT, ExperimentState.CONFIGURED) == ExperimentState.CONFIGURED


def test_aps_hypothesis_core_and_tracking() -> None:
    hyp = Hypothesis.create(
        "proj-1",
        "RSI improves Sharpe on trend strategies",
        objective="Validate RSI filter",
        success_criteria="Sharpe > 1.0",
    )
    assert hyp.status == HypothesisStatus.PENDING
    hyp.link_experiment("exp-1")
    hyp.link_strategy("strat-rsi")
    hyp.validate()
    assert hyp.status == HypothesisStatus.VALIDATED
    assert "exp-1" in hyp.linked_experiments

    registry = HypothesisRegistry()
    registry.register(hyp)
    pending = registry.list_by_status(HypothesisStatus.PENDING)
    validated = registry.list_by_status(HypothesisStatus.VALIDATED)
    assert len(pending) == 0
    assert len(validated) == 1


def test_aps_repro_capture_verify_replay() -> None:
    exp = ExperimentSpec.create("proj-1", "repro-test", dataset_version="ds-v3")
    exp.params = {"lookback": 14, "threshold": 0.7}
    original = ReproducibilityBundle.capture(
        exp,
        feature_version="feat-v2",
        strategy_version="strat-1.0.0",
        code_revision="abc123",
    )
    replay = replay_experiment_bundle(original)
    result = verify_reproducibility(original, replay)
    assert result["reproducible"] is True
    assert bundle_hash(original) == bundle_hash(replay)


def test_aps_repro_verify_detects_drift() -> None:
    exp = ExperimentSpec.create("proj-1", "drift-test", dataset_version="v1")
    original = ReproducibilityBundle.capture(exp, code_revision="abc")
    replay = ReproducibilityBundle.capture(
        ExperimentSpec.create("proj-1", "drift-test", dataset_version="v2"),
        code_revision="abc",
    )
    result = verify_reproducibility(original, replay)
    assert result["reproducible"] is False
    assert result["checks"]["dataset_version"] is False


def test_aps_exp_events_bus() -> None:
    bus = ResearchEventBus()
    evt = ResearchEvent(
        ResearchEventType.PROJECT_CREATED,
        datetime(2024, 1, 1, tzinfo=UTC),
        {"project_id": "p1"},
    )
    bus.publish(evt)
    drained = bus.drain()
    assert len(drained) == 1
    bus.replay(drained)
    assert len(bus.history) == 2


def test_aps_res_workspace_manager_integration() -> None:
    mgr = ResearchManager()
    project = mgr.create_project("QREP study", description="phase 9")
    exp = mgr.create_experiment(project.project_id, "baseline", params={"seed": 42})
    mgr.advance_experiment(exp.experiment_id, ExperimentState.CONFIGURED)
    mgr.advance_experiment(exp.experiment_id, ExperimentState.RUNNING)
    snap = mgr.capture_dataset("ohlcv", "v1", {"symbols": ["AAPL"], "rows": 500})
    assert snap.content_hash
    entry = mgr.add_knowledge(project.project_id, "Note", "Initial finding", tags=["baseline"])
    assert isinstance(entry, KnowledgeEntry)

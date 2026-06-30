"""Reproducibility engine — PHASE 9 QREP, APS-REPRO-*."""

from __future__ import annotations

import hashlib
import json
import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

from athena_core.domain.research.context import ExperimentSpec
from athena_core.domain.research.dataset import reproducibility_hash


@dataclass(frozen=True)
class ReproducibilityBundle:
    """Captured reproducibility context — APS-REPRO-BUNDLE-001."""

    bundle_id: str
    experiment_id: str
    dataset_version: str
    feature_version: str
    strategy_version: str
    parameter_hash: str
    code_revision: str
    captured_at: datetime
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def capture(
        cls,
        experiment: ExperimentSpec,
        *,
        feature_version: str = "",
        strategy_version: str = "",
        code_revision: str = "",
        metadata: dict[str, Any] | None = None,
    ) -> ReproducibilityBundle:
        """Capture reproducibility bundle from experiment — APS-REPRO-CORE-001."""
        return cls(
            bundle_id=str(uuid.uuid4()),
            experiment_id=experiment.experiment_id,
            dataset_version=experiment.dataset_version,
            feature_version=feature_version,
            strategy_version=strategy_version,
            parameter_hash=reproducibility_hash(experiment.params),
            code_revision=code_revision,
            captured_at=datetime.now(UTC),
            metadata=dict(metadata or {}),
        )


def bundle_hash(bundle: ReproducibilityBundle) -> str:
    """Deterministic bundle hash — APS-REPRO-HASH-001."""
    payload = {
        "experiment_id": bundle.experiment_id,
        "dataset_version": bundle.dataset_version,
        "feature_version": bundle.feature_version,
        "strategy_version": bundle.strategy_version,
        "parameter_hash": bundle.parameter_hash,
        "code_revision": bundle.code_revision,
    }
    encoded = json.dumps(payload, sort_keys=True).encode()
    return hashlib.sha256(encoded).hexdigest()


def verify_reproducibility(
    original: ReproducibilityBundle,
    replay: ReproducibilityBundle,
) -> dict[str, Any]:
    """Verify replay matches original — APS-REPRO-VERIFY-001."""
    checks = {
        "dataset_version": original.dataset_version == replay.dataset_version,
        "feature_version": original.feature_version == replay.feature_version,
        "strategy_version": original.strategy_version == replay.strategy_version,
        "parameter_hash": original.parameter_hash == replay.parameter_hash,
        "code_revision": original.code_revision == replay.code_revision,
    }
    return {
        "reproducible": all(checks.values()),
        "checks": checks,
        "original_hash": bundle_hash(original),
        "replay_hash": bundle_hash(replay),
    }


def replay_experiment_bundle(
    original: ReproducibilityBundle,
    *,
    experiment_id: str | None = None,
) -> ReproducibilityBundle:
    """Replay experiment from captured bundle — APS-REPRO-REPLAY-001."""
    return ReproducibilityBundle(
        bundle_id=str(uuid.uuid4()),
        experiment_id=experiment_id or original.experiment_id,
        dataset_version=original.dataset_version,
        feature_version=original.feature_version,
        strategy_version=original.strategy_version,
        parameter_hash=original.parameter_hash,
        code_revision=original.code_revision,
        captured_at=datetime.now(UTC),
        metadata={"replayed_from": original.bundle_id},
    )

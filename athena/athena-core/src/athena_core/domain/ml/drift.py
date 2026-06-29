"""Drift detection — ATH-REL-011 §5.7, REQ-ML-DRIFT-001."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class DriftReport:
    """Feature, concept, and data drift summary."""

    feature_drift: dict[str, float]
    concept_drift: float
    data_drift: float
    drift_detected: bool


def detect_drift(
    reference: pd.DataFrame,
    current: pd.DataFrame,
    *,
    target_ref: pd.Series | None = None,
    target_cur: pd.Series | None = None,
    threshold: float = 0.1,
) -> DriftReport:
    """Detect feature, concept, and data drift via distribution shift."""
    feature_drift: dict[str, float] = {}
    common_cols = [c for c in reference.columns if c in current.columns]
    for col in common_cols:
        ref_mean = float(reference[col].mean()) if len(reference) else 0.0
        cur_mean = float(current[col].mean()) if len(current) else 0.0
        denom = abs(ref_mean) + 1e-9
        feature_drift[col] = abs(cur_mean - ref_mean) / denom

    data_drift = float(np.mean(list(feature_drift.values()))) if feature_drift else 0.0

    concept_drift = 0.0
    if target_ref is not None and target_cur is not None:
        ref_rate = float(target_ref.mean()) if len(target_ref) else 0.0
        cur_rate = float(target_cur.mean()) if len(target_cur) else 0.0
        concept_drift = abs(cur_rate - ref_rate)

    drift_detected = data_drift > threshold or concept_drift > threshold
    return DriftReport(
        feature_drift=feature_drift,
        concept_drift=concept_drift,
        data_drift=data_drift,
        drift_detected=drift_detected,
    )

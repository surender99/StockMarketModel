"""Pattern architecture APS tests — PHASE-4 MSP pipeline."""

from __future__ import annotations

import numpy as np
import pandas as pd

from athena_core.domain.patterns.base import PatternDetector
from athena_core.domain.patterns.catalog import PATTERN_APS_CATALOG, lookup_by_aps_id
from athena_core.domain.patterns.metadata import build_metadata_store, lookup_metadata
from athena_core.domain.patterns.pipeline import PatternPipeline, PatternPipelineStage
from athena_core.domain.patterns.types import PatternEvent, PatternType


def _ohlcv(n: int = 60) -> pd.DataFrame:
    dates = pd.date_range("2020-01-01", periods=n, freq="B")
    close = pd.Series(100 + np.arange(n) * 0.1, index=dates)
    return pd.DataFrame(
        {
            "date": dates.date,
            "open": close.values,
            "high": close.values + 1,
            "low": close.values - 1,
            "close": close.values,
            "volume": 1000 + np.arange(n),
        }
    )


def test_pattern_pipeline_exposes_msp_stages() -> None:
    """APS-PAT-PIPELINE-001 — pipeline exposes MSP stage ordering."""
    pipeline = PatternPipeline()
    assert pipeline.stages == PatternPipeline.DEFAULT_STAGES
    assert PatternPipelineStage.CANDIDATE in pipeline.stages
    assert PatternPipelineStage.VALIDATED in pipeline.stages


def test_pattern_pipeline_validates_confidence() -> None:
    """APS-PAT-SCORE-CONFIDENCE-001 — validated stage filters low-confidence events."""
    detector = PatternDetector(
        {
            "low": lambda _df: [
                PatternEvent("low", PatternType.CANDLESTICK, 1, 0.2, {}),
            ],
            "high": lambda _df: [
                PatternEvent("high", PatternType.CANDLESTICK, 2, 0.9, {}),
            ],
        }
    )
    pipeline = PatternPipeline(detector, pattern_ids=["low", "high"])
    validated = pipeline.run_validated(_ohlcv())
    assert len(validated) == 1
    assert validated[0].pattern_id == "high"


def test_metadata_store_covers_aps_catalog() -> None:
    """APS-PAT-REGISTRY-META-001 — metadata store has entry per APS spec."""
    store = build_metadata_store()
    assert len(store) == len(PATTERN_APS_CATALOG)
    assert lookup_metadata("APS-PAT-PIPELINE-001") is not None


def test_lookup_by_aps_id_resolves_pipeline_spec() -> None:
    """APS-PAT-REGISTRY-DISCOVERY-001 — APS id lookup resolves pipeline spec."""
    entry = lookup_by_aps_id("APS-PAT-PIPELINE-001")
    assert entry is not None
    assert entry.domain == "Pattern-Architecture"
    assert entry.status == "Partial"

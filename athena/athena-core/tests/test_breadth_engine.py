"""Tests for breadth engine — REQ-MI-001."""

from __future__ import annotations

from datetime import date, timedelta

import pandas as pd

from athena_core.application.breadth_engine import BreadthEngine
from tests.memory_ohlcv_repo import MemoryOHLCVRepo


def _series(symbol: str, drift: float, days: int = 80) -> pd.DataFrame:
    start = date(2024, 1, 2)
    dates = [start + timedelta(days=i) for i in range(days)]
    close = [100 + drift * i for i in range(days)]
    return pd.DataFrame(
        {
            "date": dates,
            "open": close,
            "high": [c + 2 for c in close],
            "low": [c - 2 for c in close],
            "close": close,
            "volume": [1000] * days,
            "symbol": [symbol] * days,
        }
    )


def test_breadth_metrics_req_mi_001() -> None:
    as_of = date(2024, 1, 2) + timedelta(days=79)
    repo = MemoryOHLCVRepo(
        {
            "A": _series("A", 1.0),
            "B": _series("B", 0.5),
            "C": _series("C", -0.5),
        }
    )
    metrics = BreadthEngine(repo).compute(["A", "B", "C"], as_of)
    assert metrics.advances + metrics.declines + metrics.unchanged == 3
    assert 0 <= metrics.breadth_score <= 100
    assert metrics.pct_above_ema20 >= 0


def test_breadth_deterministic_req_mi_001() -> None:
    as_of = date(2024, 1, 2) + timedelta(days=79)
    repo = MemoryOHLCVRepo({"A": _series("A", 0.2), "B": _series("B", 0.1)})
    engine = BreadthEngine(repo)
    first = engine.compute(["A", "B"], as_of)
    second = engine.compute(["A", "B"], as_of)
    assert first == second

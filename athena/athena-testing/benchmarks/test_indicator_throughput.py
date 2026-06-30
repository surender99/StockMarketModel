"""Stub benchmark for indicator throughput — APS-IND-BENCH-100K-001."""

from __future__ import annotations

import time

import pandas as pd
import pytest

from athena_testing.golden import resolve_golden_dataset

# Performance gate: 100k rows under 2s (stub threshold, adjust per PERFORMANCE-GATES.md)
GATE_SECONDS = 2.0
TARGET_ROWS = 100_000


@pytest.mark.benchmark
def test_indicator_throughput_gate() -> None:
    """Smoke benchmark — verifies gate infrastructure, not full indicator suite."""
    base = pd.read_csv(resolve_golden_dataset("ohlcv-sample-30d.csv"))
    repeats = max(1, TARGET_ROWS // len(base))
    df = pd.concat([base] * repeats, ignore_index=True)
    assert len(df) >= min(TARGET_ROWS, len(base))

    start = time.perf_counter()
    _ = df["close"].rolling(20).mean()
    elapsed = time.perf_counter() - start

    assert elapsed < GATE_SECONDS, f"throughput gate failed: {elapsed:.3f}s > {GATE_SECONDS}s"

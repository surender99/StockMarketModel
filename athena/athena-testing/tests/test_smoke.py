"""Smoke tests for athena-testing package."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

from athena_testing.golden import GOLDEN_DATASETS_DIR, SPEC_GOLDEN_DIR, resolve_golden_dataset


def test_spec_golden_dir_exists() -> None:
    assert SPEC_GOLDEN_DIR.is_dir()


def test_resolve_ohlcv_csv() -> None:
    path = resolve_golden_dataset("ohlcv-sample-30d.csv")
    df = pd.read_csv(path)
    assert {"open", "high", "low", "close", "volume"}.issubset(df.columns)


def test_local_parquet_fixture() -> None:
    parquet = GOLDEN_DATASETS_DIR / "ohlcv-sample-30d.parquet"
    if not parquet.exists():
        pytest.skip("parquet fixture not generated")
    df = pd.read_parquet(parquet)
    assert len(df) > 0


def test_athena_os_import() -> None:
    from athena_os import EventBus

    assert EventBus().handler_count() == 0


def test_athena_core_bootstrap() -> None:
    from athena_core.application.bootstrap import bootstrap_athena_core
    from athena_core.application.config import AthenaConfig

    ctx = bootstrap_athena_core(AthenaConfig(), wire_data=False)
    assert ctx.event_bus is not None

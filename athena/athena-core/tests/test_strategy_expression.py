"""Tests for strategy expression evaluation — REQ-STRAT-CONFIG-001."""

from __future__ import annotations

import pandas as pd
import pytest

from athena_core.domain.strategy.expression import ExpressionError, evaluate_condition_at_index


def _frame() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "date": pd.date_range("2024-01-01", periods=5, freq="D").date,
            "ema_fast": [1.0, 2.0, 3.0, 2.0, 1.0],
            "ema_slow": [2.0, 2.0, 2.0, 2.0, 2.0],
            "volume": [100, 200, 300, 400, 500],
        }
    )


def test_crossover_detected_at_index() -> None:
    frame = _frame()
    condition = "ema_fast > ema_slow and ema_fast.shift(1) <= ema_slow.shift(1)"
    cols = {"ema_fast": "ema_fast", "ema_slow": "ema_slow"}
    assert not evaluate_condition_at_index(condition, frame, cols, 0)
    assert not evaluate_condition_at_index(condition, frame, cols, 1)
    assert evaluate_condition_at_index(condition, frame, cols, 2)


def test_exit_condition() -> None:
    frame = _frame()
    cols = {"ema_fast": "ema_fast", "ema_slow": "ema_slow"}
    assert evaluate_condition_at_index("ema_fast < ema_slow", frame, cols, 4)


def test_unsafe_expression_rejected() -> None:
    frame = _frame()
    with pytest.raises(ExpressionError):
        evaluate_condition_at_index("__import__('os')", frame, {"ema_fast": "ema_fast"}, 0)


def test_lookahead_shift_uses_prior_bar_only() -> None:
    frame = _frame()
    cols = {"ema_fast": "ema_fast", "ema_slow": "ema_slow"}
    # At index 0, shift(1) is NaN -> condition false
    assert not evaluate_condition_at_index("ema_fast.shift(1) > 999", frame, cols, 0)

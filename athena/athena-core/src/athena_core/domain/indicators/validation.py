"""Indicator output validation — REQ-IND-VALIDATION-001, ATH-REL-004 §12."""

from __future__ import annotations

import pandas as pd


def validate_indicator_output(
    ohlcv: pd.DataFrame,
    result: pd.Series | pd.DataFrame,
    *,
    indicator_id: str,
) -> None:
    """Ensure indicator output length matches input OHLCV rows."""
    expected = len(ohlcv)
    actual = len(result)
    if actual != expected:
        msg = f"indicator {indicator_id!r} output length {actual} != ohlcv length {expected}"
        raise ValueError(msg)

"""Execution and fill models — REQ-BT-EXECUTION-001, ATH-REL-007 §5.3."""

from __future__ import annotations

from enum import StrEnum
from typing import Any

import pandas as pd


class FillModel(StrEnum):
    """Bar fill policies — FR-002."""

    CURRENT_BAR_CLOSE = "current_bar_close"
    NEXT_BAR_OPEN = "next_bar_open"
    MARKET = "market"


def resolve_fill_price(
    frame: pd.DataFrame,
    idx: int,
    *,
    fill_model: str | FillModel,
    is_buy: bool,
    fill_price_col: str = "close",
) -> float | None:
    """Resolve raw fill price before slippage — REQ-BT-EXECUTION-001."""
    model = FillModel(fill_model) if isinstance(fill_model, str) else fill_model
    if model == FillModel.MARKET:
        model = FillModel.CURRENT_BAR_CLOSE

    if model == FillModel.CURRENT_BAR_CLOSE:
        return float(frame.iloc[idx][fill_price_col])

    if model == FillModel.NEXT_BAR_OPEN:
        if idx + 1 >= len(frame):
            return None
        return float(frame.iloc[idx + 1]["open"])

    msg = f"unsupported fill model: {model}"
    raise ValueError(msg)


def order_type_for_fill_model(fill_model: str | FillModel) -> str:
    """Map fill policy to default order type."""
    model = FillModel(fill_model) if isinstance(fill_model, str) else fill_model
    if model == FillModel.NEXT_BAR_OPEN:
        return "market"
    return "market"


def bar_for_execution(
    frame: pd.DataFrame,
    session_idx: int,
    *,
    fill_model: str | FillModel,
) -> tuple[int, dict[str, Any]] | None:
    """Return bar index and row for order execution on a session."""
    model = FillModel(fill_model) if isinstance(fill_model, str) else fill_model
    if model in (FillModel.CURRENT_BAR_CLOSE, FillModel.MARKET):
        if session_idx >= len(frame):
            return None
        row = frame.iloc[session_idx]
        return session_idx, row.to_dict()
    if model == FillModel.NEXT_BAR_OPEN:
        next_idx = session_idx + 1
        if next_idx >= len(frame):
            return None
        row = frame.iloc[next_idx]
        return next_idx, row.to_dict()
    return None

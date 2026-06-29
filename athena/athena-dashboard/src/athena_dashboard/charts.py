"""Dashboard chart engine — ATH-REL-013, REQ-DASH-CHART-001."""

from __future__ import annotations

from typing import Any

import pandas as pd


def build_candlestick_data(ohlcv: pd.DataFrame) -> list[dict[str, Any]]:
    """Prepare OHLCV rows for candlestick rendering."""
    required = {"open", "high", "low", "close"}
    if not required.issubset(set(c.lower() for c in ohlcv.columns)):
        cols = {c.lower(): c for c in ohlcv.columns}
        if not required.issubset(cols):
            return []
    normalized = ohlcv.rename(columns=str.lower)
    rows: list[dict[str, Any]] = []
    for _, row in normalized.iterrows():
        rows.append(
            {
                "open": float(row["open"]),
                "high": float(row["high"]),
                "low": float(row["low"]),
                "close": float(row["close"]),
                "volume": float(row.get("volume", 0)),
            }
        )
    return rows


def build_heatmap(matrix: pd.DataFrame) -> dict[str, Any]:
    """Correlation-style heatmap payload."""
    if matrix.empty:
        return {"labels": [], "values": []}
    corr = matrix.corr() if matrix.select_dtypes("number").shape[1] > 1 else matrix
    return {
        "labels": list(corr.columns),
        "values": corr.values.tolist(),
    }


def build_bar_chart(labels: list[str], values: list[float]) -> dict[str, Any]:
    """Simple bar chart payload."""
    return {"labels": labels, "values": values}

"""OHLCV data quality checks — REQ-DATA-QUALITY-001, AES-0310."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

import pandas as pd


class DataQualityIssue(str, Enum):
    """Quality check failure categories — AES-0310."""

    MISSING_CANDLES = "missing_candles"
    DUPLICATE_ROWS = "duplicate_rows"
    INVALID_OHLC = "invalid_ohlc"
    ZERO_VOLUME = "zero_volume"
    OUTLIER = "outlier"


@dataclass
class DataQualityReport:
    """Result of OHLCV quality validation."""

    symbol: str
    row_count: int
    issues: list[DataQualityIssue] = field(default_factory=list)
    details: dict[str, int | float | list[str]] = field(default_factory=dict)

    @property
    def passed(self) -> bool:
        return len(self.issues) == 0


def check_ohlcv_quality(
    df: pd.DataFrame,
    symbol: str = "",
    *,
    outlier_z_threshold: float = 5.0,
) -> DataQualityReport:
    """Validate OHLCV DataFrame before feature generation — AES-0310."""
    report = DataQualityReport(symbol=symbol, row_count=len(df))
    if df.empty:
        report.issues.append(DataQualityIssue.MISSING_CANDLES)
        report.details["empty"] = True
        return report

    required = {"date", "open", "high", "low", "close", "volume"}
    missing_cols = required - set(df.columns)
    if missing_cols:
        report.issues.append(DataQualityIssue.INVALID_OHLC)
        report.details["missing_columns"] = sorted(missing_cols)
        return report

    dup_count = int(df.duplicated(subset=["date"]).sum())
    if dup_count > 0:
        report.issues.append(DataQualityIssue.DUPLICATE_ROWS)
        report.details["duplicate_count"] = dup_count

    invalid_ohlc = (
        (df["high"] < df["low"])
        | (df["high"] < df["open"])
        | (df["high"] < df["close"])
        | (df["low"] > df["open"])
        | (df["low"] > df["close"])
    )
    invalid_count = int(invalid_ohlc.sum())
    if invalid_count > 0:
        report.issues.append(DataQualityIssue.INVALID_OHLC)
        report.details["invalid_ohlc_count"] = invalid_count

    zero_vol = int((df["volume"] == 0).sum())
    if zero_vol > 0:
        report.issues.append(DataQualityIssue.ZERO_VOLUME)
        report.details["zero_volume_count"] = zero_vol

    # Outlier detection on close returns
    returns = df["close"].pct_change().dropna()
    if len(returns) > 1 and returns.std() > 0:
        z = (returns - returns.mean()).abs() / returns.std()
        outlier_count = int((z > outlier_z_threshold).sum())
        if outlier_count > 0:
            report.issues.append(DataQualityIssue.OUTLIER)
            report.details["outlier_count"] = outlier_count

    return report


def compute_quality_score(report: DataQualityReport) -> float:
    """Composite 0–100 quality score — REQ-APS-DQ-SCORE-001."""
    if report.row_count == 0:
        return 0.0
    penalty = 0.0
    weights = {
        DataQualityIssue.MISSING_CANDLES: 40.0,
        DataQualityIssue.DUPLICATE_ROWS: 15.0,
        DataQualityIssue.INVALID_OHLC: 25.0,
        DataQualityIssue.ZERO_VOLUME: 10.0,
        DataQualityIssue.OUTLIER: 10.0,
    }
    for issue in report.issues:
        penalty += weights.get(issue, 5.0)
    return max(0.0, min(100.0, 100.0 - penalty))


def profile_ohlcv_frame(df: pd.DataFrame) -> dict[str, int | float]:
    """Column-level profiler summary — REQ-APS-DQ-PROFILER-001."""
    if df.empty:
        return {"row_count": 0}
    summary: dict[str, int | float] = {"row_count": len(df)}
    for col in ("open", "high", "low", "close", "volume"):
        if col not in df.columns:
            continue
        series = df[col]
        summary[f"{col}_null_count"] = int(series.isna().sum())
        if col != "volume":
            summary[f"{col}_min"] = float(series.min())
            summary[f"{col}_max"] = float(series.max())
    return summary

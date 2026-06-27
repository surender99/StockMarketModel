"""Application configuration models — REQ-DATA-INGEST-001, REQ-FEAT-STORE-001."""

from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, Field

from athena_core.application.backtest_config import BacktestSettings, ExperimentTrackingConfig


class CalendarConfig(BaseModel):
    """REQ-DATA-CALENDAR-001."""

    exchange: str = "NSE"
    timezone: str = "Asia/Kolkata"
    holidays_file: Path = Field(default=Path("./config/nse_holidays.yaml"))
    weekend_days: list[str] = Field(default_factory=lambda: ["Saturday", "Sunday"])


class DataIngestConfig(BaseModel):
    """REQ-DATA-INGEST-001."""

    source: str = "yfinance"
    base_path: Path = Field(default=Path("./data/ohlcv"))
    symbol_suffix: str = ".NS"
    bar_frequency: str = "1d"
    max_attempts: int = 3
    backoff_seconds: float = 2.0
    schema_columns: list[str] = Field(
        default_factory=lambda: ["date", "open", "high", "low", "close", "volume", "symbol"]
    )


class IndicatorConfig(BaseModel):
    """REQ-IND-EMA-001 / REQ-IND-SMA-001 defaults."""

    ema_periods: list[int] = Field(default_factory=lambda: [9, 21, 50, 200])
    sma_periods: list[int] = Field(default_factory=lambda: [20, 50, 200])
    price_column: str = "close"


class FeatureStoreConfig(BaseModel):
    """REQ-FEAT-STORE-001."""

    base_path: Path = Field(default=Path("./data/features"))
    compression: str = "snappy"
    data_version: str = "v1"


class AthenaConfig(BaseModel):
    """Root configuration bundle."""

    calendar: CalendarConfig = Field(default_factory=CalendarConfig)
    data_ingest: DataIngestConfig = Field(default_factory=DataIngestConfig)
    indicators: IndicatorConfig = Field(default_factory=IndicatorConfig)
    feature_store: FeatureStoreConfig = Field(default_factory=FeatureStoreConfig)
    backtest: BacktestSettings = Field(default_factory=BacktestSettings)
    experiment_tracking: ExperimentTrackingConfig = Field(default_factory=ExperimentTrackingConfig)

"""Application configuration models — REQ-DATA-INGEST-001, REQ-FEAT-STORE-001, ATH-REL-002."""

from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, Field

from athena_common.timeframe import TimeFrame
from athena_core.application.backtest_config import BacktestSettings, ExperimentTrackingConfig
from athena_core.application.explainability_config import ExplainabilityConfig
from athena_core.application.ml_scorer_config import MLScorerConfig
from athena_core.application.optimizer_config import OptimizerConfig
from athena_core.application.regime_config import RegimeConfig
from athena_core.application.scanner_config import ScannerConfig
from athena_core.application.walk_forward_config import WalkForwardConfig
from athena_core.application.core_config import CoreFrameworkConfig
from athena_core.domain.features.caching import FeatureCachePolicy
from athena_core.application.data_platform_config import DataPlatformConfig


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
    bar_frequency: str = TimeFrame.D1.value
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
    """REQ-FEAT-STORE-001, REQ-FEAT-CACHE-001."""

    base_path: Path = Field(default=Path("./data/features"))
    compression: str = "snappy"
    data_version: str = "v1"
    cache_policy: FeatureCachePolicy = FeatureCachePolicy.COMPUTE_ON_MISS


class AthenaConfig(BaseModel):
    """Root configuration bundle."""

    calendar: CalendarConfig = Field(default_factory=CalendarConfig)
    data_ingest: DataIngestConfig = Field(default_factory=DataIngestConfig)
    indicators: IndicatorConfig = Field(default_factory=IndicatorConfig)
    feature_store: FeatureStoreConfig = Field(default_factory=FeatureStoreConfig)
    backtest: BacktestSettings = Field(default_factory=BacktestSettings)
    experiment_tracking: ExperimentTrackingConfig = Field(default_factory=ExperimentTrackingConfig)
    regime: RegimeConfig = Field(default_factory=RegimeConfig)
    scanner: ScannerConfig = Field(default_factory=ScannerConfig)
    walk_forward: WalkForwardConfig = Field(default_factory=WalkForwardConfig)
    optimizer: OptimizerConfig = Field(default_factory=OptimizerConfig)
    ml_scorer: MLScorerConfig = Field(default_factory=MLScorerConfig)
    explainability: ExplainabilityConfig = Field(default_factory=ExplainabilityConfig)
    core: CoreFrameworkConfig = Field(default_factory=CoreFrameworkConfig)
    data_platform: DataPlatformConfig = Field(default_factory=DataPlatformConfig)

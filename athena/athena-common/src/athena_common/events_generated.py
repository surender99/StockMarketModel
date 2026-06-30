"""AUTO-GENERATED — do not edit by hand.

Source: athena-spec/events/registry/*.event.yaml
Regenerate: make codegen  OR  python athena/scripts/generate_events.py
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, ClassVar

@dataclass(frozen=True, slots=True)
class DataValidatedEvent:
    """OHLCV frame passed quality checks — v1, publisher=Data."""

    EVENT_NAME: ClassVar[str] = 'DataValidated'
    VERSION: ClassVar[int] = 1
    PUBLISHER: ClassVar[str] = 'Data'
    CONSUMERS: ClassVar[tuple[str, ...]] = ('Ingest', 'Registry')

    symbol: str
    quality_score: float
    issue_count: int

@dataclass(frozen=True, slots=True)
class FeatureComputedEvent:
    """Feature vector computed for a symbol — v1, publisher=FeaturePipeline."""

    EVENT_NAME: ClassVar[str] = 'FeatureComputed'
    VERSION: ClassVar[int] = 1
    PUBLISHER: ClassVar[str] = 'FeaturePipeline'
    CONSUMERS: ClassVar[tuple[str, ...]] = ('Strategy', 'Research')

    symbol: str
    feature_set_id: str
    row_count: int

@dataclass(frozen=True, slots=True)
class IndicatorCalculatedEvent:
    """Indicator values computed for a symbol — v1, publisher=Indicator."""

    EVENT_NAME: ClassVar[str] = 'IndicatorCalculated'
    VERSION: ClassVar[int] = 1
    PUBLISHER: ClassVar[str] = 'Indicator'
    CONSUMERS: ClassVar[tuple[str, ...]] = ('Pattern', 'Strategy')

    symbol: str
    indicator_id: str
    timeframe: str
    row_count: int

@dataclass(frozen=True, slots=True)
class IndicatorRegisteredEvent:
    """New indicator plugin registered — v1, publisher=Indicator."""

    EVENT_NAME: ClassVar[str] = 'IndicatorRegistered'
    VERSION: ClassVar[int] = 1
    PUBLISHER: ClassVar[str] = 'Indicator'
    CONSUMERS: ClassVar[tuple[str, ...]] = ('PluginRegistry')

    indicator_id: str
    version: str
    author: str

@dataclass(frozen=True, slots=True)
class IngestCompletedEvent:
    """Historical ingest finished successfully — v1, publisher=Data."""

    EVENT_NAME: ClassVar[str] = 'IngestCompleted'
    VERSION: ClassVar[int] = 1
    PUBLISHER: ClassVar[str] = 'Data'
    CONSUMERS: ClassVar[tuple[str, ...]] = ('FeaturePipeline', 'DatasetRegistry')

    symbol: str
    rows: int
    source: str
    bar_frequency: str

@dataclass(frozen=True, slots=True)
class IngestFailedEvent:
    """Historical ingest failed — v1, publisher=Data."""

    EVENT_NAME: ClassVar[str] = 'IngestFailed'
    VERSION: ClassVar[int] = 1
    PUBLISHER: ClassVar[str] = 'Data'
    CONSUMERS: ClassVar[tuple[str, ...]] = ('Observability', 'RetryJobs')

    symbol: str
    error: str
    source: str

@dataclass(frozen=True, slots=True)
class PatternDetectedEvent:
    """Chart or candlestick pattern detected — v1, publisher=Pattern."""

    EVENT_NAME: ClassVar[str] = 'PatternDetected'
    VERSION: ClassVar[int] = 1
    PUBLISHER: ClassVar[str] = 'Pattern'
    CONSUMERS: ClassVar[tuple[str, ...]] = ('Strategy', 'Dashboard')

    symbol: str
    pattern_id: str
    confidence: float
    bar_index: int

@dataclass(frozen=True, slots=True)
class PortfolioRebalancedEvent:
    """Portfolio rebalance completed — v1, publisher=Portfolio."""

    EVENT_NAME: ClassVar[str] = 'PortfolioRebalanced'
    VERSION: ClassVar[int] = 1
    PUBLISHER: ClassVar[str] = 'Portfolio'
    CONSUMERS: ClassVar[tuple[str, ...]] = ('Risk', 'Audit')

    portfolio_id: str
    turnover: float
    position_count: int

@dataclass(frozen=True, slots=True)
class ResearchExperimentStartedEvent:
    """Research experiment execution started — v1, publisher=Research."""

    EVENT_NAME: ClassVar[str] = 'ResearchExperimentStarted'
    VERSION: ClassVar[int] = 1
    PUBLISHER: ClassVar[str] = 'Research'
    CONSUMERS: ClassVar[tuple[str, ...]] = ('Reproducibility', 'Events')

    project_id: str
    experiment_id: str
    hypothesis_id: str

@dataclass(frozen=True, slots=True)
class SecurityAuditEvent:
    """Security audit trail entry — v1, publisher=AthenaOS."""

    EVENT_NAME: ClassVar[str] = 'SecurityAudit'
    VERSION: ClassVar[int] = 1
    PUBLISHER: ClassVar[str] = 'AthenaOS'
    CONSUMERS: ClassVar[tuple[str, ...]] = ('Compliance', 'Logging')

    actor: str
    action: str
    resource: str
    outcome: str

@dataclass(frozen=True, slots=True)
class SignalGeneratedEvent:
    """Trade signal emitted by strategy engine — v1, publisher=Strategy."""

    EVENT_NAME: ClassVar[str] = 'SignalGenerated'
    VERSION: ClassVar[int] = 1
    PUBLISHER: ClassVar[str] = 'Strategy'
    CONSUMERS: ClassVar[tuple[str, ...]] = ('Backtest', 'PaperTrading')

    strategy_id: str
    symbol: str
    direction: str
    strength: float

@dataclass(frozen=True, slots=True)
class SimulationOrderEvent:
    """Simulated order lifecycle event — v1, publisher=Execution."""

    EVENT_NAME: ClassVar[str] = 'SimulationOrder'
    VERSION: ClassVar[int] = 1
    PUBLISHER: ClassVar[str] = 'Execution'
    CONSUMERS: ClassVar[tuple[str, ...]] = ('TradeJournal', 'Portfolio')

    order_id: str
    symbol: str
    side: str
    quantity: int
    status: str

@dataclass(frozen=True, slots=True)
class StrategyEvaluatedEvent:
    """Strategy evaluation cycle completed — v1, publisher=Strategy."""

    EVENT_NAME: ClassVar[str] = 'StrategyEvaluated'
    VERSION: ClassVar[int] = 1
    PUBLISHER: ClassVar[str] = 'Strategy'
    CONSUMERS: ClassVar[tuple[str, ...]] = ('Portfolio', 'Reporting')

    strategy_id: str
    symbol: str
    signal_count: int
    passed_risk: bool


EVENT_REGISTRY: dict[str, type] = {
    'DataValidated': DataValidatedEvent,
    'FeatureComputed': FeatureComputedEvent,
    'IndicatorCalculated': IndicatorCalculatedEvent,
    'IndicatorRegistered': IndicatorRegisteredEvent,
    'IngestCompleted': IngestCompletedEvent,
    'IngestFailed': IngestFailedEvent,
    'PatternDetected': PatternDetectedEvent,
    'PortfolioRebalanced': PortfolioRebalancedEvent,
    'ResearchExperimentStarted': ResearchExperimentStartedEvent,
    'SecurityAudit': SecurityAuditEvent,
    'SignalGenerated': SignalGeneratedEvent,
    'SimulationOrder': SimulationOrderEvent,
    'StrategyEvaluated': StrategyEvaluatedEvent,
}

__all__ = [
    "DataValidatedEvent",
    "FeatureComputedEvent",
    "IndicatorCalculatedEvent",
    "IndicatorRegisteredEvent",
    "IngestCompletedEvent",
    "IngestFailedEvent",
    "PatternDetectedEvent",
    "PortfolioRebalancedEvent",
    "ResearchExperimentStartedEvent",
    "SecurityAuditEvent",
    "SignalGeneratedEvent",
    "SimulationOrderEvent",
    "StrategyEvaluatedEvent",
    "EVENT_REGISTRY",
]

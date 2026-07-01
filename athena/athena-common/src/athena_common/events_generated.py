# GENERATED — DO NOT EDIT
# Source: athena-spec/events/registry/*.event.yaml
# Regenerate: make codegen  OR  python athena/scripts/generate_events.py

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
    SCHEMA: ClassVar[dict[str, Any]] = {'type': 'object', 'required': ['symbol', 'quality_score', 'issue_count'], 'properties': {'symbol': {'type': 'string'}, 'quality_score': {'type': 'number'}, 'issue_count': {'type': 'integer'}}}

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
    SCHEMA: ClassVar[dict[str, Any]] = {'type': 'object', 'required': ['symbol', 'feature_set_id', 'row_count'], 'properties': {'symbol': {'type': 'string'}, 'feature_set_id': {'type': 'string'}, 'row_count': {'type': 'integer'}}}

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
    SCHEMA: ClassVar[dict[str, Any]] = {'type': 'object', 'required': ['symbol', 'indicator_id', 'timeframe', 'row_count'], 'properties': {'symbol': {'type': 'string'}, 'indicator_id': {'type': 'string'}, 'timeframe': {'type': 'string'}, 'row_count': {'type': 'integer'}}}

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
    SCHEMA: ClassVar[dict[str, Any]] = {'type': 'object', 'required': ['indicator_id', 'version', 'author'], 'properties': {'indicator_id': {'type': 'string'}, 'version': {'type': 'string'}, 'author': {'type': 'string'}}}

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
    SCHEMA: ClassVar[dict[str, Any]] = {'type': 'object', 'required': ['symbol', 'rows', 'source', 'bar_frequency'], 'properties': {'symbol': {'type': 'string'}, 'rows': {'type': 'integer'}, 'source': {'type': 'string'}, 'bar_frequency': {'type': 'string'}}}

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
    SCHEMA: ClassVar[dict[str, Any]] = {'type': 'object', 'required': ['symbol', 'error', 'source'], 'properties': {'symbol': {'type': 'string'}, 'error': {'type': 'string'}, 'source': {'type': 'string'}}}

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
    SCHEMA: ClassVar[dict[str, Any]] = {'type': 'object', 'required': ['symbol', 'pattern_id', 'confidence', 'bar_index'], 'properties': {'symbol': {'type': 'string'}, 'pattern_id': {'type': 'string'}, 'confidence': {'type': 'number'}, 'bar_index': {'type': 'integer'}}}

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
    SCHEMA: ClassVar[dict[str, Any]] = {'type': 'object', 'required': ['portfolio_id', 'turnover', 'position_count'], 'properties': {'portfolio_id': {'type': 'string'}, 'turnover': {'type': 'number'}, 'position_count': {'type': 'integer'}}}

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
    SCHEMA: ClassVar[dict[str, Any]] = {'type': 'object', 'required': ['project_id', 'experiment_id', 'hypothesis_id'], 'properties': {'project_id': {'type': 'string'}, 'experiment_id': {'type': 'string'}, 'hypothesis_id': {'type': 'string'}}}

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
    SCHEMA: ClassVar[dict[str, Any]] = {'type': 'object', 'required': ['actor', 'action', 'resource', 'outcome'], 'properties': {'actor': {'type': 'string'}, 'action': {'type': 'string'}, 'resource': {'type': 'string'}, 'outcome': {'type': 'string'}}}

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
    SCHEMA: ClassVar[dict[str, Any]] = {'type': 'object', 'required': ['strategy_id', 'symbol', 'direction', 'strength'], 'properties': {'strategy_id': {'type': 'string'}, 'symbol': {'type': 'string'}, 'direction': {'type': 'string'}, 'strength': {'type': 'number'}}}

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
    SCHEMA: ClassVar[dict[str, Any]] = {'type': 'object', 'required': ['order_id', 'symbol', 'side', 'quantity', 'status'], 'properties': {'order_id': {'type': 'string'}, 'symbol': {'type': 'string'}, 'side': {'type': 'string'}, 'quantity': {'type': 'integer'}, 'status': {'type': 'string'}}}

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
    SCHEMA: ClassVar[dict[str, Any]] = {'type': 'object', 'required': ['strategy_id', 'symbol', 'signal_count', 'passed_risk'], 'properties': {'strategy_id': {'type': 'string'}, 'symbol': {'type': 'string'}, 'signal_count': {'type': 'integer'}, 'passed_risk': {'type': 'boolean'}}}

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

"""Domain events — facade over athena-core and generated contracts."""

from athena_common.events_generated import EVENT_REGISTRY
from athena_core.domain.events import DomainEvent, EventBus, EventHandler

__all__ = ["DomainEvent", "EventBus", "EventHandler", "EVENT_REGISTRY"]

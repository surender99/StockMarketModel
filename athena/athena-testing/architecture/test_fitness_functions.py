"""Architecture fitness functions — API and event compatibility stubs."""

from __future__ import annotations

from athena_common.events_generated import EVENT_REGISTRY, IndicatorCalculatedEvent


def test_event_registry_has_catalog_events() -> None:
    assert "IndicatorCalculated" in EVENT_REGISTRY
    assert IndicatorCalculatedEvent.VERSION >= 1


def test_event_payload_fields_present() -> None:
    fields = IndicatorCalculatedEvent.__dataclass_fields__
    assert "symbol" in fields
    assert "indicator_id" in fields


def test_api_compat_stub() -> None:
    """Placeholder for interface catalog version checks."""
    assert True

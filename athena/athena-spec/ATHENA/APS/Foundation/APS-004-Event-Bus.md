# APS-004 — Event Bus

> **APS ID:** APS-004  
> **Requirement ID:** REQ-APS-004  
> **Maps to:** REQ-CORE-EVT-001  
> **Phase:** 1 — Foundation  
> **Source:** `References/PHASE1 -ATHENA FOUNDATION APS.docx`

## Objective

In-process publish/subscribe for domain and application events.

## Responsibilities

- Publish events
- Subscribe handlers
- Handler priority ordering
- Error propagation policy

## Public API

- `EventBus`
- `Event`
- `subscribe`
- `publish`

## Functional Requirements

- **FR-001:** Subscribe handler to event type
- **FR-002:** Publish delivers to all subscribers
- **FR-003:** Unsubscribe or one-shot handlers
- **FR-004:** Handler failure surfaces as EventError

## Code Wiring (`athena-core`)

- `athena-core/src/athena_core/domain/events/`

## Configuration

See [ATH-REL-001](../../ATH-REL-001-Core-Framework.md) and [release-01/](../../release-01/README.md).

## Dependencies

- ATH-REL-000 Engineering Standards
- ATH-REL-001 Core Framework
- ATH-004 Requirement Standard

## Acceptance Criteria

- [ ] Multiple subscribers receive same event
- [ ] Unregistered event type does not crash publish
- [ ] Handler exception wrapped with ErrorCode.EVENT

## Performance Target

N/A

## Unit Tests

- `test_core_framework.py::test_event_bus_*`

## Integration Tests

- Bootstrap path via `AthenaRuntime` and CLI where applicable

## Future Enhancements

- Full provider plugins per APS-004 source document
- Dedicated `athena-core/foundation/` package layout (target structure in source doc)

---

*Template: [ATH-004 Requirement Standard](../../ATH-004-Requirement-Standard.md)*

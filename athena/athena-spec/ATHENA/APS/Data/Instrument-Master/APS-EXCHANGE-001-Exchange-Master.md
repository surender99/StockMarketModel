# APS-EXCHANGE-001 — Exchange Master

> **APS ID:** APS-EXCHANGE-001  
> **Requirement ID:** REQ-APS-EXCHANGE-001  
> **Maps to:** REQ-DATA-CALENDAR-001  
> **Phase:** 2 — Data Platform  
> **Domain:** Instrument Master  
> **Source:** `References/PHASE2 -DATA PLATFORM APS.docx`  
> **Implementation status:** Partial

## Objective

Exchange Master for the Athena data platform (instrument master domain).

## Responsibilities

- Trading hours
- Timezones
- Sessions
- Auction periods
- Holiday calendars

## Code Wiring (`athena-core`)

- `athena-core/src/athena_core/infrastructure/nse_calendar.py`

## Target Layout (future `athena-data` packages)

Per CTO recommendation in source document:

- `athena-data-core` — contracts, schemas, calendars, symbols
- `athena-data-connectors` — Yahoo, NSE, Polygon, broker adapters
- `athena-data-engine` — validation, cleaning, aggregation, feature store
- `athena-data-services` — import/export orchestration

Current MVP consolidates into `athena-core` per [ATH-003](../../ATH-003-Repository-Architecture.md).

## Dependencies

- Phase 1 Foundation APS (APS-001–015)
- ATH-REL-002 Data Platform
- ATH-004 Requirement Standard

## Acceptance Criteria

- [ ] Core subset of APS-EXCHANGE-001 implemented
- [ ] Deferred capabilities documented in spec
- [ ] Maps to REQ-DATA-CALENDAR-001 where applicable

## Unit Tests

- `tests/test_data_platform.py`
- `tests/test_data_quality.py`

## Future Enhancements

- Extract to dedicated `athena-data-*` packages when connector surface grows
- Full coverage of all responsibilities listed in source document

---

*Template: [ATH-004 Requirement Standard](../../ATH-004-Requirement-Standard.md)*

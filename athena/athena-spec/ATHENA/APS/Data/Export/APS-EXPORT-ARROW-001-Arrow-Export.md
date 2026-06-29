# APS-EXPORT-ARROW-001 — Arrow Export

> **APS ID:** APS-EXPORT-ARROW-001  
> **Requirement ID:** REQ-APS-EXPORT-ARROW-001  
> **Maps to:** REQ-DATA-INGEST-001  
> **Phase:** 2 — Data Platform  
> **Domain:** Export  
> **Source:** `References/PHASE2 -DATA PLATFORM APS.docx`  
> **Implementation status:** Deferred

## Objective

Arrow Export for the Athena data platform (export domain).

## Responsibilities

- Arrow IPC export

## Code Wiring (`athena-core`)

- 📋 Not yet implemented in `athena-core`

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

- [ ] APS-EXPORT-ARROW-001 spec published with REQ ID
- [ ] Deferred — no silent stub in production path
- [ ] Future implementation traces to REQ-DATA-INGEST-001

## Unit Tests

- Future domain tests under `tests/test_data_*.py`

## Future Enhancements

- Extract to dedicated `athena-data-*` packages when connector surface grows
- Full coverage of all responsibilities listed in source document

---

*Template: [ATH-004 Requirement Standard](../../ATH-004-Requirement-Standard.md)*

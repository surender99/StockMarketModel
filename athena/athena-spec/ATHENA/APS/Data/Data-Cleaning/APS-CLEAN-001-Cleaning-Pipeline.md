# APS-CLEAN-001 — Cleaning Pipeline

> **APS ID:** APS-CLEAN-001  
> **Requirement ID:** REQ-APS-CLEAN-001  
> **Maps to:** REQ-DATA-CLEAN-001  
> **Phase:** 2 — Data Platform  
> **Domain:** Data Cleaning  
> **Source:** `References/PHASE2 -DATA PLATFORM APS.docx`  
> **Implementation status:** MVP

## Objective

Cleaning Pipeline for the Athena data platform (data cleaning domain).

## Responsibilities

- Remove duplicates
- Sort
- Normalize

## Code Wiring (`athena-core`)

- `athena-core/src/athena_core/domain/data/cleaning.py`

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

- [ ] APS-CLEAN-001 responsibilities covered by wired `athena-core` modules
- [ ] Maps to REQ-DATA-CLEAN-001 acceptance criteria
- [ ] Unit tests pass for implemented behavior

## Unit Tests

- `tests/test_data_platform.py`
- `tests/test_data_quality.py`

## Future Enhancements

- Extract to dedicated `athena-data-*` packages when connector surface grows
- Full coverage of all responsibilities listed in source document

---

*Template: [ATH-004 Requirement Standard](../../ATH-004-Requirement-Standard.md)*

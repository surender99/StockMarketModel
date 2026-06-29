# APS-010 — Type System

> **APS ID:** APS-010  
> **Requirement ID:** REQ-APS-010  
> **Maps to:** REQ-CORE-UTL-001  
> **Phase:** 1 — Foundation  
> **Source:** `References/PHASE1 -ATHENA FOUNDATION APS.docx`

## Objective

Strong domain types — no primitive obsession for money, symbols, versions.

## Responsibilities

- Semantic newtypes (Identifier, SemanticVersion)
- Date normalization
- Exchange symbol conventions
- Future: Money, Price, Quantity types

## Public API

- `Identifier`
- `SemanticVersion`
- `ensure_date`
- `utc_now`

## Functional Requirements

- **FR-001:** Normalize date inputs to date
- **FR-002:** UTC timestamps for audit fields
- **FR-003:** Type hints on all public APIs

## Code Wiring (`athena-core`)

- `athena-core/src/athena_core/domain/common/`

## Configuration

See [ATH-REL-001](../../ATH-REL-001-Core-Framework.md) and [release-01/](../../release-01/README.md).

## Dependencies

- ATH-REL-000 Engineering Standards
- ATH-REL-001 Core Framework
- ATH-004 Requirement Standard

## Acceptance Criteria

- [ ] ensure_date accepts date, datetime, ISO str
- [ ] Invalid date input raises TypeError
- [ ] Public APIs fully type-hinted per ATH-002

## Performance Target

N/A

## Unit Tests

- `test_core_framework.py`

## Integration Tests

- Bootstrap path via `AthenaRuntime` and CLI where applicable

## Future Enhancements

- Full provider plugins per APS-010 source document
- Dedicated `athena-core/foundation/` package layout (target structure in source doc)

---

*Template: [ATH-004 Requirement Standard](../../ATH-004-Requirement-Standard.md)*

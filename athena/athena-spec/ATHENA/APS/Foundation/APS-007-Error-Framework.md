# APS-007 — Error Framework

> **APS ID:** APS-007  
> **Requirement ID:** REQ-APS-007  
> **Maps to:** REQ-CORE-ERR-001  
> **Phase:** 1 — Foundation  
> **Source:** `References/PHASE1 -ATHENA FOUNDATION APS.docx`

## Objective

Unified exception hierarchy with stable error codes and context.

## Responsibilities

- Domain vs infrastructure errors
- Stable ErrorCode enum
- Structured context dict
- Retry hints (future)

## Public API

- `AthenaError`
- `ConfigurationError`
- `ValidationError`
- `NotFoundError`
- `PluginError`
- `ErrorCode`

## Functional Requirements

- **FR-001:** All errors carry ErrorCode
- **FR-002:** Context dict serializes in __str__
- **FR-003:** Hierarchy: AthenaError → domain subclasses

## Code Wiring (`athena-core`)

- `athena-core/src/athena_core/domain/errors.py`

## Configuration

See [ATH-REL-001](../../ATH-REL-001-Core-Framework.md) and [release-01/](../../release-01/README.md).

## Dependencies

- ATH-REL-000 Engineering Standards
- ATH-REL-001 Core Framework
- ATH-004 Requirement Standard

## Acceptance Criteria

- [ ] ConfigurationError uses ATH-CFG-001
- [ ] ValidationError uses ATH-VAL-001
- [ ] str(error) includes code and context

## Performance Target

N/A

## Unit Tests

- `test_core_framework.py::test_error_*`

## Integration Tests

- Bootstrap path via `AthenaRuntime` and CLI where applicable

## Future Enhancements

- Full provider plugins per APS-007 source document
- Dedicated `athena-core/foundation/` package layout (target structure in source doc)

---

*Template: [ATH-004 Requirement Standard](../../ATH-004-Requirement-Standard.md)*

# APS-005 — Registry Framework

> **APS ID:** APS-005  
> **Requirement ID:** REQ-APS-005  
> **Maps to:** REQ-CORE-PLG-001  
> **Phase:** 1 — Foundation  
> **Source:** `References/PHASE1 -ATHENA FOUNDATION APS.docx`

## Objective

Central registry for versioned, searchable plugin and artifact metadata.

## Responsibilities

- Register items with metadata
- Lookup by id and aliases
- Version tagging
- Search/list operations

## Public API

- `PluginRegistry`
- `DatasetRegistry`
- `InstrumentMaster`

## Functional Requirements

- **FR-001:** Register with unique id
- **FR-002:** Lookup by id
- **FR-003:** List all in namespace
- **FR-004:** Attach semantic version metadata

## Code Wiring (`athena-core`)

- `athena-core/src/athena_core/domain/plugins/registry.py`
- `athena-core/src/athena_core/domain/data/registry.py`
- `athena-core/src/athena_core/infrastructure/instrument_master.py`

## Configuration

See [ATH-REL-001](../../ATH-REL-001-Core-Framework.md) and [release-01/](../../release-01/README.md).

## Dependencies

- ATH-REL-000 Engineering Standards
- ATH-REL-001 Core Framework
- ATH-004 Requirement Standard

## Acceptance Criteria

- [ ] Register + lookup round-trip
- [ ] Duplicate id rejected
- [ ] List returns registered keys

## Performance Target

N/A

## Unit Tests

- `test_core_framework.py`
- `test_data_platform.py`

## Integration Tests

- Bootstrap path via `AthenaRuntime` and CLI where applicable

## Future Enhancements

- Full provider plugins per APS-005 source document
- Dedicated `athena-core/foundation/` package layout (target structure in source doc)

---

*Template: [ATH-004 Requirement Standard](../../ATH-004-Requirement-Standard.md)*

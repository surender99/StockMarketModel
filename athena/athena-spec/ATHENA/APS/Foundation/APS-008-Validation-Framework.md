# APS-008 — Validation Framework

> **APS ID:** APS-008  
> **Requirement ID:** REQ-APS-008  
> **Maps to:** REQ-CORE-ERR-001  
> **Phase:** 1 — Foundation  
> **Source:** `References/PHASE1 -ATHENA FOUNDATION APS.docx`

## Objective

Schema and business validation for configs, strategies, and data.

## Responsibilities

- Pydantic schema validation
- Business rule validation
- Cross-field validation
- Runtime validation at boundaries

## Public API

- `ValidationError`
- `StrategyConfig validators`
- `Pydantic models`

## Functional Requirements

- **FR-001:** Reject invalid strategy YAML
- **FR-002:** Reject invalid OHLCV schema
- **FR-003:** Return ValidationError with field context

## Code Wiring (`athena-core`)

- `athena-core/src/athena_core/domain/strategy/config.py`
- `athena-core/src/athena_core/domain/strategy/validation.py`
- `athena-core/src/athena_core/domain/data/quality.py`

## Configuration

See [ATH-REL-001](../../ATH-REL-001-Core-Framework.md) and [release-01/](../../release-01/README.md).

## Dependencies

- ATH-REL-000 Engineering Standards
- ATH-REL-001 Core Framework
- ATH-004 Requirement Standard

## Acceptance Criteria

- [ ] Invalid strategy config raises ValidationError
- [ ] Data quality checks flag missing columns
- [ ] Pydantic models enforce types at load

## Performance Target

N/A

## Unit Tests

- `test_strategy_config.py`
- `test_data_platform.py`

## Integration Tests

- Bootstrap path via `AthenaRuntime` and CLI where applicable

## Future Enhancements

- Full provider plugins per APS-008 source document
- Dedicated `athena-core/foundation/` package layout (target structure in source doc)

---

*Template: [ATH-004 Requirement Standard](../../ATH-004-Requirement-Standard.md)*

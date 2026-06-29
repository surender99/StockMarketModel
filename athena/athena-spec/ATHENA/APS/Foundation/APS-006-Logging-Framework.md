# APS-006 — Logging Framework

> **APS ID:** APS-006  
> **Requirement ID:** REQ-APS-006  
> **Maps to:** REQ-CORE-LOG-001  
> **Phase:** 1 — Foundation  
> **Source:** `References/PHASE1 -ATHENA FOUNDATION APS.docx`

## Objective

Structured logging with JSON and text outputs for all Athena services.

## Responsibilities

- Structured logging
- JSON log format
- Console output
- Log level configuration
- Trace/correlation id hooks (future)

## Public API

- `configure_logging`
- `structlog`

## Functional Requirements

- **FR-001:** Configure root log level from config
- **FR-002:** Emit JSON logs when json_logs=true
- **FR-003:** Emit human-readable text when json_logs=false

## Code Wiring (`athena-core`)

- `athena-core/src/athena_core/infrastructure/logging.py`

## Configuration

See [ATH-REL-001](../../ATH-REL-001-Core-Framework.md) and [release-01/](../../release-01/README.md).

## Dependencies

- ATH-REL-000 Engineering Standards
- ATH-REL-001 Core Framework
- ATH-004 Requirement Standard

## Acceptance Criteria

- [ ] Logging configures without error at bootstrap
- [ ] JSON mode produces parseable log lines
- [ ] Level filter respects config

## Performance Target

N/A

## Unit Tests

- `test_core_framework.py`

## Integration Tests

- Bootstrap path via `AthenaRuntime` and CLI where applicable

## Future Enhancements

- Full provider plugins per APS-006 source document
- Dedicated `athena-core/foundation/` package layout (target structure in source doc)

---

*Template: [ATH-004 Requirement Standard](../../ATH-004-Requirement-Standard.md)*

# APS-002 — Dependency Injection

> **APS ID:** APS-002  
> **Requirement ID:** REQ-APS-002  
> **Maps to:** REQ-CORE-DI-001  
> **Phase:** 1 — Foundation  
> **Source:** `References/PHASE1 -ATHENA FOUNDATION APS.docx`

## Objective

Dependency injection container for composable Athena services.

## Responsibilities

- Service registration
- Service discovery
- Constructor/factory injection
- Singleton lifecycle
- Scoped lifecycle (transient factory)

## Public API

- `ServiceContainer`
- `bootstrap_athena_core`
- `CoreContext`

## Functional Requirements

- **FR-001:** Register factory by service key
- **FR-002:** Resolve singleton instance once
- **FR-003:** Resolve transient new instance each call
- **FR-004:** Reject duplicate registration
- **FR-005:** Raise NotFoundError for unknown service

## Code Wiring (`athena-core`)

- `athena-core/src/athena_core/application/container.py`
- `athena-core/src/athena_core/application/bootstrap.py`

## Configuration

See [ATH-REL-001](../../ATH-REL-001-Core-Framework.md) and [release-01/](../../release-01/README.md).

## Dependencies

- ATH-REL-000 Engineering Standards
- ATH-REL-001 Core Framework
- ATH-004 Requirement Standard

## Acceptance Criteria

- [ ] Singleton returns same instance on repeated resolve
- [ ] Transient returns new instance each resolve
- [ ] Factory injection registers callables
- [ ] Duplicate key registration raises ConfigurationError
- [ ] bootstrap_athena_core wires config, plugins, event_bus

## Performance Target

N/A — in-process registry

## Unit Tests

- `test_core_framework.py::test_container_*`
- `test_bootstrap_wires_core_context`

## Integration Tests

- Bootstrap path via `AthenaRuntime` and CLI where applicable

## Future Enhancements

- Full provider plugins per APS-002 source document
- Dedicated `athena-core/foundation/` package layout (target structure in source doc)

---

*Template: [ATH-004 Requirement Standard](../../ATH-004-Requirement-Standard.md)*

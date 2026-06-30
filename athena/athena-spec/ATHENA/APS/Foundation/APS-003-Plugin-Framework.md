# APS-003 — Plugin Framework

## Traceability

| Field | Value |
|-------|-------|
| **APS ID** | APS-003 |
| **Implemented In** | `athena/athena-os/src/athena_os/plugins.py` |
| **Tests** | `athena-os/tests/test_athena_os.py`, `athena-core/tests/test_plugin_registry.py` |
| **Benchmarks** | N/A |
| **Owner** | `@platform` |
| **Status** | MVP |
| **Release** | REL-001 |
| **Example** | `PluginRegistry().register(Plugin(...))` |

> **APS ID:** APS-003  
> **Requirement ID:** REQ-APS-003  
> **Maps to:** REQ-CORE-PLG-001  
> **Phase:** 1 — Foundation  
> **Source:** `References/PHASE1 -ATHENA FOUNDATION APS.docx`

## Objective

Discover and load Athena plugins dynamically across domains.

## Responsibilities

- Discovery and registration
- Loading built-in plugins
- Version metadata
- Lifecycle hooks
- Dependency ordering
- Isolation via registry keys

## Public API

- `PluginRegistry`
- `register_builtin_*`

## Functional Requirements

- **FR-001:** Register plugin by domain key
- **FR-002:** Lookup plugin by id
- **FR-003:** List plugins per domain
- **FR-004:** Reject duplicate plugin ids
- **FR-005:** Recover from missing optional plugin

## Code Wiring (`athena-core`)

- `athena-core/src/athena_core/domain/plugins/registry.py`
- `athena-core/src/athena_core/domain/features/indicator_plugins.py`
- `athena-core/src/athena_core/domain/strategy/strategy_plugins.py`

## Configuration

See [ATH-REL-001](../../ATH-REL-001-Core-Framework.md) and [release-01/](../../release-01/README.md).

## Dependencies

- ATH-REL-000 Engineering Standards
- ATH-REL-001 Core Framework
- ATH-004 Requirement Standard

## Acceptance Criteria

- [ ] Built-in indicators register at bootstrap
- [ ] Lookup returns callable plugin
- [ ] Unknown plugin id raises PluginError or NotFoundError
- [ ] Domains isolated (indicator vs strategy keys)

## Performance Target

N/A

## Unit Tests

- `test_core_framework.py`
- `test_indicator_framework.py`

## Integration Tests

- Bootstrap path via `AthenaRuntime` and CLI where applicable

## Future Enhancements

- Full provider plugins per APS-003 source document
- Dedicated `athena-core/foundation/` package layout (target structure in source doc)

---

*Template: [ATH-004 Requirement Standard](../../ATH-004-Requirement-Standard.md)*

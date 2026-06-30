# APS-IND-REGISTRY-001 — Indicator Registry

> **APS ID:** APS-IND-REGISTRY-001  
> **Requirement ID:** REQ-APS-IND-REGISTRY-001  
> **Maps to:** REQ-FEAT-REGISTRY-001  
> **Phase:** 3 — Indicators  
> **Domain:** Indicator Registry  
> **Source:** `References/ATH-REL-004-Indicator-Framework.zip (inferred PHASE-3)`  
> **Implementation status:** MVP

## Objective

Indicator Registry for the Athena indicators (indicator registry domain).

## Responsibilities

- Builtin indicator registration
- Plugin discovery
- Configuration schema

## Code Wiring (`athena-core`)

- `athena-core/src/athena_core/domain/features/indicator_plugins.py`
- `athena-core/src/athena_core/domain/indicators/catalog.py`

## Dependencies

- Phase 1 Foundation APS (APS-001–015)
- Phase 2 Data Platform APS
- ATH-REL-004-Indicator-Framework.md

## Acceptance Criteria

- [ ] APS-IND-REGISTRY-001 responsibilities covered by wired `athena-core` modules
- [ ] Maps to REQ-FEAT-REGISTRY-001 where applicable
- [ ] Unit tests pass for implemented behavior

## Unit Tests

`tests/test_indicator_framework.py`, `tests/test_indicator_aps.py`

## Future Enhancements

- Full coverage of all responsibilities listed in source release package
- Extract to dedicated packages when surface area grows

---

*Template: [ATH-004 Requirement Standard](../../ATH-004-Requirement-Standard.md)*

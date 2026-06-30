# APS-PAT-REGISTRY-META-001 — Pattern Metadata Store

> **APS ID:** APS-PAT-REGISTRY-META-001  
> **Requirement ID:** REQ-APS-PAT-REGISTRY-META-001  
> **Phase:** 4 — Patterns  
> **Domain:** Pattern Registry  
> **Source:** `References/PHASE4 - Market Structure & Pattern Intelligence Platform (MSP).docx`  
> **Implementation status:** MVP

## Objective

Pattern Metadata Store for the Athena patterns platform (pattern registry domain).

## Responsibilities

- Pattern Metadata Store
- OHLCV input contract
- Pattern detection pipeline integration
- Confidence metadata

## Code Wiring (`athena-core`)

- `athena-core/src/athena_core/domain/patterns/catalog.py`
- `athena-core/src/athena_core/domain/patterns/pipeline.py`

## Dependencies

- Phase 1 Foundation APS (APS-001–015)
- Phase 2 Data Platform APS
- Phase 3 Indicators APS
- [ATH-REL-005-Pattern-Recognition.md](../../ATH-REL-005-Pattern-Recognition.md)

## Acceptance Criteria

- [ ] APS-PAT-REGISTRY-META-001 spec published with REQ ID
- [ ] MVP modules wired where status is MVP/Partial
- [ ] Deferred APS have no silent production stub

## Unit Tests

`tests/test_pattern_recognition_framework.py`, `tests/test_pattern_aps.py`, `tests/test_phase45_aps.py`

---

*Template: [ATH-004 Requirement Standard](../../ATH-004-Requirement-Standard.md)*

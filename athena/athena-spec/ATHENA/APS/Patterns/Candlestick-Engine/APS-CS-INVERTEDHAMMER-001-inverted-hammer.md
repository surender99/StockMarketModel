# APS-CS-INVERTEDHAMMER-001 — Inverted Hammer

> **APS ID:** APS-CS-INVERTEDHAMMER-001  
> **Requirement ID:** REQ-APS-CS-INVERTEDHAMMER-001  
> **Phase:** 4 — Patterns  
> **Domain:** Candlestick Engine  
> **Source:** `References/PHASE4 - Market Structure & Pattern Intelligence Platform (MSP).docx`  
> **Implementation status:** MVP

## Objective

Inverted Hammer for the Athena patterns platform (candlestick engine domain).

## Responsibilities

- Inverted Hammer
- OHLCV input contract
- Pattern detection pipeline integration
- Confidence metadata

## Code Wiring (`athena-core`)

- `athena-core/src/athena_core/domain/patterns/candlestick.py`

## Dependencies

- Phase 1 Foundation APS (APS-001–015)
- Phase 2 Data Platform APS
- Phase 3 Indicators APS
- [ATH-REL-005-Pattern-Recognition.md](../../ATH-REL-005-Pattern-Recognition.md)

## Acceptance Criteria

- [ ] APS-CS-INVERTEDHAMMER-001 spec published with REQ ID
- [ ] MVP modules wired where status is MVP/Partial
- [ ] Deferred APS have no silent production stub

## Unit Tests

`tests/test_pattern_recognition_framework.py`, `tests/test_pattern_aps.py`, `tests/test_phase45_aps.py`

---

*Template: [ATH-004 Requirement Standard](../../ATH-004-Requirement-Standard.md)*

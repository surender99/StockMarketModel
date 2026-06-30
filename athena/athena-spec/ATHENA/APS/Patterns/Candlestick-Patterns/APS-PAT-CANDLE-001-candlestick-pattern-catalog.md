# APS-PAT-CANDLE-001 — Candlestick Pattern Catalog

> **APS ID:** APS-PAT-CANDLE-001  
> **Requirement ID:** REQ-APS-PAT-CANDLE-001  
> **Maps to:** REQ-PAT-001  
> **Phase:** 4 — Patterns  
> **Domain:** Candlestick Patterns  
> **Source:** `References/ATH-REL-005-Pattern-Recognition.zip (inferred PHASE-4)`  
> **Implementation status:** MVP

## Objective

Candlestick Pattern Catalog for the Athena patterns (candlestick patterns domain).

## Responsibilities

- Hammer
- Engulfing
- Doji
- Star patterns
- Harami

## Code Wiring (`athena-core`)

- `athena-core/src/athena_core/domain/patterns/candlestick.py`

## Dependencies

- Phase 1 Foundation APS (APS-001–015)
- Phase 2 Data Platform APS
- ATH-REL-005-Pattern-Recognition.md

## Acceptance Criteria

- [ ] APS-PAT-CANDLE-001 responsibilities covered by wired `athena-core` modules
- [ ] Maps to REQ-PAT-001 where applicable
- [ ] Unit tests pass for implemented behavior

## Unit Tests

`tests/test_pattern_recognition_framework.py`, `tests/test_pattern_aps.py`

## Future Enhancements

- Full coverage of all responsibilities listed in source release package
- Extract to dedicated packages when surface area grows

---

*Template: [ATH-004 Requirement Standard](../../ATH-004-Requirement-Standard.md)*

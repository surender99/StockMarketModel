# APS-IND-NVI-001 — Negative Volume Index

> **APS ID:** APS-IND-NVI-001  
> **Requirement ID:** REQ-APS-IND-NVI-001  
> **Maps to:** REQ-IND-IND-NVI-001  
> **Phase:** 3 — Indicators  
> **Domain:** Volume Indicators  
> **Source:** `References/PHASE 3 Architecture.docx`  
> **Implementation status:** Deferred

## Objective

Negative Volume Index for the Athena indicators platform (volume indicators domain).

## Responsibilities

- Negative Volume Index computation
- Configurable parameters
- OHLCV input contract
- NaN/warmup policy

## Code Wiring (`athena-core`)

- *(deferred — no MVP wiring yet)*

## Dependencies

- Phase 1 Foundation APS (APS-001–015)
- Phase 2 Data Platform APS
- ATH-REL-004-Indicator-Framework.md

## Acceptance Criteria

- [ ] APS-IND-NVI-001 spec published with REQ ID
- [ ] Deferred — no silent stub in production path
- [ ] Future implementation traces to REQ-IND-IND-NVI-001

## Unit Tests

`tests/test_indicator_framework.py`, `tests/test_indicator_aps.py`, `tests/test_indicator_architecture.py`

## Future Enhancements

- Full coverage per Indicator Specification Standard (formula, validation, benchmarks)
- Layered architecture: formulas / execution / adapters separation per CTO recommendation

---

*Template: [ATH-004 Requirement Standard](../../ATH-004-Requirement-Standard.md)*

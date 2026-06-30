# APS-IND-MFI-001 — Money Flow Index

> **APS ID:** APS-IND-MFI-001  
> **Requirement ID:** REQ-APS-IND-MFI-001  
> **Maps to:** REQ-IND-IND-MFI-001  
> **Phase:** 3 — Indicators  
> **Domain:** Volume Indicators  
> **Source:** `References/PHASE 3 Architecture.docx`  
> **Implementation status:** MVP

## Objective

Money Flow Index for the Athena indicators platform (volume indicators domain).

## Responsibilities

- Money Flow Index computation
- Configurable parameters
- OHLCV input contract
- NaN/warmup policy

## Code Wiring (`athena-core`)

- `athena-core/src/athena_core/domain/indicators/mfi.py`

## Dependencies

- Phase 1 Foundation APS (APS-001–015)
- Phase 2 Data Platform APS
- ATH-REL-004-Indicator-Framework.md

## Acceptance Criteria

- [ ] APS-IND-MFI-001 responsibilities covered by wired `athena-core` modules
- [ ] Maps to REQ-IND-IND-MFI-001 where applicable
- [ ] Unit tests pass for implemented behavior

## Unit Tests

`tests/test_indicator_framework.py`, `tests/test_indicator_aps.py`, `tests/test_indicator_architecture.py`

## Future Enhancements

- Full coverage per Indicator Specification Standard (formula, validation, benchmarks)
- Layered architecture: formulas / execution / adapters separation per CTO recommendation

---

*Template: [ATH-004 Requirement Standard](../../ATH-004-Requirement-Standard.md)*

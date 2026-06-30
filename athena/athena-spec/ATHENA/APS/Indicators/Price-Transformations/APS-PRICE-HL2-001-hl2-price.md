# APS-PRICE-HL2-001 — HL2 Price

> **APS ID:** APS-PRICE-HL2-001  
> **Requirement ID:** REQ-APS-PRICE-HL2-001  
> **Maps to:** REQ-IND-PRICE-HL2-001  
> **Phase:** 3 — Indicators  
> **Domain:** Price Transformations  
> **Source:** `References/PHASE 3 Architecture.docx`  
> **Implementation status:** MVP

## Objective

HL2 Price for the Athena indicators platform (price transformations domain).

## Responsibilities

- HL2 Price computation
- Configurable parameters
- OHLCV input contract
- NaN/warmup policy

## Code Wiring (`athena-core`)

- `athena-core/src/athena_core/domain/indicators/price_transforms.py`

## Dependencies

- Phase 1 Foundation APS (APS-001–015)
- Phase 2 Data Platform APS
- ATH-REL-004-Indicator-Framework.md

## Acceptance Criteria

- [ ] APS-PRICE-HL2-001 responsibilities covered by wired `athena-core` modules
- [ ] Maps to REQ-IND-PRICE-HL2-001 where applicable
- [ ] Unit tests pass for implemented behavior

## Unit Tests

`tests/test_indicator_framework.py`, `tests/test_indicator_aps.py`, `tests/test_indicator_architecture.py`

## Future Enhancements

- Full coverage per Indicator Specification Standard (formula, validation, benchmarks)
- Layered architecture: formulas / execution / adapters separation per CTO recommendation

---

*Template: [ATH-004 Requirement Standard](../../ATH-004-Requirement-Standard.md)*

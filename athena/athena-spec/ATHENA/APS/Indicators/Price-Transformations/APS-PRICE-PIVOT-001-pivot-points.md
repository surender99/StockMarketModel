# APS-PRICE-PIVOT-001 — Pivot Points

> **APS ID:** APS-PRICE-PIVOT-001  
> **Requirement ID:** REQ-APS-PRICE-PIVOT-001  
> **Maps to:** REQ-IND-PRICE-PIVOT-001  
> **Phase:** 3 — Indicators  
> **Domain:** Price Transformations  
> **Source:** `References/PHASE 3 Architecture.docx`  
> **Implementation status:** MVP

## Objective

Classic floor-trader pivot support/resistance levels from prior bar HLC.

## Responsibilities

- Pivot, R1–R3, S1–S3 computation
- OHLCV input contract
- NaN policy for first bar (no prior HLC)

## Code Wiring (`athena-core`)

- `athena-core/src/athena_core/domain/indicators/pivot_points.py`

## Dependencies

- Phase 1 Foundation APS (APS-001–015)
- Phase 2 Data Platform APS
- ATH-REL-004-Indicator-Framework.md

## Acceptance Criteria

- [ ] APS-PRICE-PIVOT-001 responsibilities covered by wired `athena-core` modules
- [ ] Maps to REQ-IND-PRICE-PIVOT-001 where applicable
- [ ] Unit tests pass for implemented behavior

## Unit Tests

`tests/test_indicators_deferred.py`, `tests/test_indicator_architecture.py`

## Future Enhancements

- Fibonacci and Camarilla pivot variants
- Layered architecture: formulas / execution / adapters separation per CTO recommendation

---

*Template: [ATH-004 Requirement Standard](../../ATH-004-Requirement-Standard.md)*

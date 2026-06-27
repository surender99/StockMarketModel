# DEC-002 – References Packages 01–15 Spec Integration

> **Date:** 2026-06-27  
> **Status:** Accepted  
> **Related:** [REFERENCES-INTEGRATION-COMPLETE.md](../REFERENCES-INTEGRATION-COMPLETE.md), [REFERENCES-INDEX.md](../REFERENCES-INDEX.md)

## Decision

Integrate all **References packages 01–15** into canonical paths under `athena/athena-spec/` (and Package 15 handbook under `athena/athena-docs/handbook/`). The `References/` directory at repo root remains **read-only source**; never edit in place.

## Integration approach

1. Copy or merge markdown specs into domain folders (`market-intelligence/`, `backtesting/`, etc.).
2. Preserve AES document IDs for traceability.
3. Cross-link ATH docs where overlap exists — avoid blind duplication.
4. Produce one `packages/PACKAGE-NN-COMPLETE.md` validation report per package.
5. Close **code gaps only where explicitly required** for MVP (e.g. MACD/RSI, data quality, pattern stub).

## Rationale

References packages are the authoritative design corpus. Integrating into `athena-spec/` keeps specs beside code and REQ backlog in one monorepo without multi-repo sync.

## Consequences

- "Package NN complete" in REFERENCES-INDEX means **spec integration complete**, not necessarily full code for that domain.
- See [SPEC-VS-CODE-STATUS.md](../SPEC-VS-CODE-STATUS.md) for spec vs implementation gaps.

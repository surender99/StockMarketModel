# DEC-003 – Hybrid Requirements Layout

> **Date:** 2026-06-27  
> **Status:** Accepted  
> **Related:** [requirements/README.md](../requirements/README.md), [ATH-004 Requirement Standard](../ATH-004-Requirement-Standard.md)

## Decision

Use a **hybrid requirements layout**:

1. **Flat top-level** — `athena/athena-spec/requirements/` holds cross-cutting and MVP-phase REQs (e.g. `REQ-DATA-INGEST-001`, `REQ-SDK-001`).
2. **Per-package folders** — domain REQs live under package spec trees (e.g. `feature-engineering/requirements/REQ-IND-MACD-001.md`, `portfolio-engine/requirements/REQ-PF-001.md`).

Do **not** mass-move files into a single flat directory.

## Rationale

MVP phases were tracked from a single backlog; References integration added domain-scoped REQs beside AES specs. Moving everything would break links in validation reports and PLATFORM-COMPLETE tables without adding traceability value.

## Consequences

- New MVP-wide REQs → `requirements/`.
- New domain REQs → `<package>/requirements/` with cross-links from flat index when needed.
- REQ IDs remain globally unique regardless of folder.

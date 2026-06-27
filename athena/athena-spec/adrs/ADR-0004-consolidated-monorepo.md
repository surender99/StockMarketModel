# ADR-0004 – Consolidated Monorepo Packages

> **Status:** Accepted  
> **Date:** 2026-06-27  
> **Deciders:** Athena platform architects

## Context

Athena spans governance specs, core quant engines, SDK, CLI, dashboard, and AI assistant. The team is small and phases 0–7 deliver a single research platform, not independently versioned products. Repository boundaries must minimize cross-repo coordination while preserving clean architecture layers.

## Decision

Use a **single consolidated monorepo** under `athena/` with multiple installable Python packages:

- **`athena-core`** — domain, application, and infrastructure (market intelligence, research, ML logic lives here)
- **`athena-sdk`** — public `AthenaClient` facade
- **`athena-cli`**, **`athena-dashboard`**, **`athena-ai`** — interface adapters
- **`athena-spec`**, **`athena-docs`** — specifications and handbook (non-Python)

Do **not** split market/research/ML into separate Git repositories for the MVP.

## Alternatives Considered

| Option | Pros | Cons |
|--------|------|------|
| **Consolidated monorepo** (chosen) | Atomic refactors; single CI; shared REQ traceability; matches ATH-003 | Larger clone; all packages share release cadence unless versioned independently later |
| **Core repo + spec repo** | Specs decoupled from code | Broken links; duplicate CI; harder REQ ↔ code traceability |
| **Per-domain repos (data, strategy, ML)** | Team autonomy at scale | Integration tax; premature for MVP; violates current phase delivery model |
| **Polyrepo with git submodules** | Theoretical isolation | Submodule friction; poor DX for solo/small team |

## Consequences

- **Positive:** One `pytest` + ruff + mypy pipeline; `AthenaClient` can evolve with core without cross-repo PRs; References integration lands in `athena-spec/` beside code.
- **Negative:** Contributors see a large tree; discipline required to keep interface packages thin.
- **Neutral:** Future extraction of a package (e.g. standalone data SDK) remains possible behind stable ports.

## Compliance

- [x] [ATH-003 Repository Architecture](../ATH-003-Repository-Architecture.md) layers respected
- [ ] [AES-0005 Quant Standards](../governance/AES-0005-Quant-Standards.md) (if research-impacting)
- [ ] Related REQ or RFC linked below

## References

- [ATH-003 Repository Architecture](../ATH-003-Repository-Architecture.md)
- [AES-0203 Repository Structure](../architecture/AES-0203-Repository-Structure.md)

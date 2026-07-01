# Agent Coordination — Parallel Workstream Ownership

> **Purpose:** Prevent duplicate agent work after parallel sessions (2026-06-30).  
> **Baseline:** `157ea98` on `master` (milestone implementation complete)

---

## Workstream Status

| Agent / Session | Scope | Status | Commit / Artifact |
|-----------------|-------|--------|-------------------|
| **9d5b8832** — Platform architecture | ADR-0006 bounded contexts: `athena-common`, `athena-domain`, facades (`athena-data` … `athena-platform`), codegen, event registry, Makefile | **DONE** | `a6585a6` |
| **ce68dfb1** — Milestone zip References | ATH-Milestone-1…17 spec trees under `athena-spec/ATHENA/Milestones/`, `MILESTONE-*-COMPLETE.md` | **DONE** | `7a7b803` |
| **1a3cc939** — Gap analysis | Read-only audit; no repo writes | **DONE** | (no commit) |
| **45ad587c** — End-to-end milestone implementation | Full M1–M17 code delivery | **DONE** | `157ea98` |

**Dedup note (2026-07-01):** Agent 45ad587c left duplicate `M01-*` … `M17-*` spec folders (untracked, removed) and duplicate `MILESTONE-N-TITLE-COMPLETE.md` sign-offs (removed; canonical names are `MILESTONE-N-COMPLETE.md`). Canonical spec folders: `Milestone-01-*` … `Milestone-17-*`.

---

## Single Ownership — Remaining Work

| Workstream | Owner (one agent path) | Do NOT parallelize |
|------------|------------------------|--------------------|
| **Milestone code implementation** | **Complete** — agent 45ad587c at `157ea98` | Do not re-implement |
| **Bounded context extraction (ADR-0006 Phase 2)** | **Architecture Agent** — move logic from `athena-core` into facades incrementally | Same module file (e.g. `athena-indicators/engine.py`) |
| **References / spec integration** | **References Agent** — zip → `athena-spec` only | Already complete; no re-integration |
| **QA / regression** | **QA Agent** — `make test`, golden datasets | N/A |

### Milestone implementation agent — entry criteria

1. Read `MILESTONE-N-COMPLETE.md` and linked spec under `ATHENA/Milestones/`.
2. Check [SPEC-VS-CODE-STATUS.md](../SPEC-VS-CODE-STATUS.md) — **do not re-implement** if code MVP already exists.
3. Implement only **gaps** listed in the milestone sign-off acceptance gate.
4. One milestone per PR/session unless explicitly scoped.

---

## Coordination Rules

1. **One agent per milestone** (M01–M17) and **one agent per bounded-context package** at a time.
2. **No parallel agents** on `athena-platform`, `athena-core` bootstrap, or `Makefile` / install tooling.
3. **Spec integration is frozen** — do not re-extract `References/*.zip` (scratch dirs `.tmp-extract*` are gitignored).
4. **Before coding:** `git pull` and read this file + latest `MILESTONE-*-COMPLETE.md`.
5. **After coding:** `make fix-editable-shadows && make test` from `athena/`.
6. **Do not** start full milestone re-implementation when sign-off says "spec integration; code MVP/Deferred".

---

## What Exists Today (honest)

| Layer | State |
|-------|-------|
| **Specs** | PHASE 1–15 APS, ATH-000A–D, REL-000–020, Milestones 1–17 — **complete** |
| **Code** | `athena-core` MVP + facade packages (ADR-0006 Phase 1) — **MVP** per [SPEC-VS-CODE-STATUS.md](../SPEC-VS-CODE-STATUS.md) |
| **Platform** | `athena-platform` runtime wiring — **MVP** |
| **Milestone code** | M1–M17 MVP implemented — **DONE** at `157ea98` (agent 45ad587c) |

---

## Milestone Implementation — Complete

All M1–M17 MVP code delivered at `157ea98` (agent 45ad587c, 2026-07-01). See `MILESTONE-N-*-COMPLETE.md` sign-offs and `athena-testing/tests/test_milestones.py` for traceability.

**Do not re-implement.** Future work is ADR-0006 Phase 2 extraction and APS catalog depth — not milestone re-delivery.

---

## Scratch / Local-Only (not in git)

- `References/*.zip` — source archives (gitignored)
- `.tmp-extract/`, `.tmp-extract-batch2/`, `.tmp-milestone-*/` — agent extraction scratch (gitignored)

---

## Contact / Handoff

Update this file when a workstream completes or ownership changes. Include commit SHA and date.

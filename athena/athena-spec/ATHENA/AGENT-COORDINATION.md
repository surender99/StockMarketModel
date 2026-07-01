# Agent Coordination — Parallel Workstream Ownership

> **Purpose:** Prevent duplicate agent work after parallel sessions (2026-06-30).  
> **Baseline:** `7a7b803` on `master` (post dedup commit if applied).

---

## Workstream Status

| Agent / Session | Scope | Status | Commit / Artifact |
|-----------------|-------|--------|-------------------|
| **9d5b8832** — Platform architecture | ADR-0006 bounded contexts: `athena-common`, `athena-domain`, facades (`athena-data` … `athena-platform`), codegen, event registry, Makefile | **DONE** | `a6585a6` |
| **ce68dfb1** — Milestone zip References | ATH-Milestone-1…17 spec trees under `athena-spec/ATHENA/Milestones/`, `MILESTONE-*-COMPLETE.md` | **DONE** | `7a7b803` |
| **1a3cc939** — Gap analysis | Read-only audit; no repo writes | **DONE** | (no commit) |
| **45ad587c** — End-to-end milestone implementation | Full M1–M17 code delivery | **NOT STARTED** (spec-only integration exists) | — |

**No duplicate packages or duplicate milestone spec trees in git.** Two sequential commits; no merge conflicts.

---

## Single Ownership — Remaining Work

| Workstream | Owner (one agent path) | Do NOT parallelize |
|------------|------------------------|--------------------|
| **Milestone code implementation** | **Milestone Implementation Agent** — one milestone at a time, M1 → M17 order | Same milestone number or same `athena-*` package |
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
| **Code** | `athena-core` MVP + facade packages (ADR-0006 Phase 1) — **partial** per [SPEC-VS-CODE-STATUS.md](../SPEC-VS-CODE-STATUS.md) |
| **Platform** | `athena-platform` runtime wiring smoke tests — **MVP** |
| **Milestone code** | M1 engineering scripts exist; M2–M17 mostly **spec + traceability tests** |

---

## Remaining Milestone Work (high level)

| MS | Title | Code gap (owner: Milestone Implementation Agent) |
|----|-------|--------------------------------------------------|
| M01 | Engineering Platform | Validators/inspector exist; deepen per ATH-010–019 |
| M02 | AthenaOS | `athena-os` MVP; promote plugins/workflow per spec |
| M03 | Data Platform | `athena-data` facade; split connectors per ATH-005 |
| M04–M09 | Indicators → OMS | Facades exist; extract from `athena-core` per ADR-0006 |
| M10 | Live Trading | `athena-platform` + production gateway stubs |
| M11–M12 | AI / Dashboard | `athena-ai`, `athena-dashboard` MVP expansion |
| M13–M17 | Enterprise | DevOps, security, ecosystem — mostly **stub → production** |

---

## Scratch / Local-Only (not in git)

- `References/*.zip` — source archives (gitignored)
- `.tmp-extract/`, `.tmp-extract-batch2/`, `.tmp-milestone-*/` — agent extraction scratch (gitignored)

---

## Contact / Handoff

Update this file when a workstream completes or ownership changes. Include commit SHA and date.

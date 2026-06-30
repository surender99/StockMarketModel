# AI Agent Roles

> **Purpose:** Standard agent workflow for Athena development with AI coding assistants.

## Role Pipeline

```
Planner → Architect → Developer → Reviewer → QA → Documentation → Release
```

| Role | Responsibility | Outputs |
|------|----------------|---------|
| **Planner** | Break REL/APS scope into tasks; prioritize | Task list, acceptance criteria |
| **Architect** | Validate design against ADRs, dependency rules | Design notes, ADR drafts |
| **Developer** | Implement code against APS specs | PR, unit tests |
| **Reviewer** | Code review, security, quant correctness | Review comments, approval |
| **QA** | Run pytest, golden datasets, benchmarks | Test report |
| **Documentation** | Update APS traceability, README, catalogs | Spec updates |
| **Release** | Version bump, changelog, production checklist | Release tag, sign-off |

## Handoff Rules

1. Planner references APS ID and TRACEABILITY-INDEX row before coding.
2. Architect confirms no dependency rule violations (`check_dependencies.py`).
3. Developer links **Implemented In** and **Tests** in APS markdown.
4. QA runs `make test` including `athena-os` and `athena-testing`.
5. Documentation updates EVENT-CATALOG and INTERFACE-CATALOG for new public APIs.
6. Release verifies [PRODUCTION-READINESS-CHECKLIST.md](../Reviews/PRODUCTION-READINESS-CHECKLIST.md).

## Prompts

Agent prompts indexed under [Prompts/README.md](README.md).

# ATH-REL-000 Engineering Standards — Section Index

> **Release package:** [ATH-REL-000-Engineering-Standards.md](../ATH-REL-000-Engineering-Standards.md)  
> **Source zip:** `References/ATH-REL-000-Engineering-Standards-v0.1.zip`

This index maps the ATH-REL-000 Release-00 folder taxonomy to canonical specs and repo tooling. Do not duplicate content here — follow the links.

---

## Section Map

| Section | Zip Status (v0.1) | Canonical Spec | Repo Tooling |
|---------|-------------------|----------------|--------------|
| **00 Constitution** | Placeholder | [ATH-000](../ATH-000-Philosophy.md), [AES-0001](../governance/AES-0001-Constitution.md) | — |
| **01 Governance** | Placeholder | [governance/](../governance/), [adrs/](../adrs/) | — |
| **02 Repository** | Placeholder | [ATH-003](../ATH-003-Repository-Architecture.md) | Monorepo `athena/` layout |
| **03 Architecture** | Placeholder | [architecture/](../architecture/) | Clean Architecture in `athena-core/src/` |
| **04 Coding** | Placeholder | [ATH-002](../ATH-002-Engineering-Standards.md) | ruff, mypy, type hints |
| **05 Documentation** | Placeholder | [ATH-004](../ATH-004-Requirement-Standard.md) | REQ specs, docstrings |
| **06 Requirements** | Placeholder | [requirements/](../requirements/), [templates/Requirement-Template.md](../templates/Requirement-Template.md) | — |
| **07 AI Development** | Placeholder | [AES-0006](../governance/AES-0006-AI-Coding-Standards.md) | [prompts/](../prompts/) |
| **08 Testing** | Placeholder | [ATH-002](../ATH-002-Engineering-Standards.md) | pytest, `@pytest.mark.integration`, `@pytest.mark.benchmark` |
| **09 Benchmarks** | Placeholder | [athena-core/benchmarks/](../../athena-core/benchmarks/README.md) | `tests/benchmarks/test_performance.py` |
| **10 Quality Gates** | Placeholder | [Definition of Done](../checklists/Definition-of-Done.md) | CI, pre-commit |
| **11 Templates** | Placeholder | [templates/](../templates/) | — |
| **12 Playbooks** | Placeholder | [athena-docs/handbook/](../../athena-docs/handbook/) | — |
| **13 ADR & RFC** | Placeholder | [adrs/](../adrs/), [templates/ADR-Template.md](../templates/ADR-Template.md) | — |
| **14 Release Management** | Placeholder | [CHANGELOG.md](../../../CHANGELOG.md) | Git tags, PLATFORM-COMPLETE |
| **15 Master Index** | Placeholder | [README.md](../README.md), [REFERENCES-INDEX](../REFERENCES-INDEX.md) | — |

---

## Quality Gate Summary (Release-00)

Enforced in CI (`.github/workflows/ci.yml`) and locally via pre-commit (`.pre-commit-config.yaml`):

| Gate | Tool | Scope |
|------|------|-------|
| Unit tests | pytest | All `athena/*` packages |
| Coverage | pytest-cov | `athena-core` |
| Lint | ruff check | All packages `src/` and `tests/` |
| Format | ruff format | All packages `src/` and `tests/` |
| Type check | mypy (strict) | `athena-core` |
| Pre-commit | trailing-whitespace, yaml, ruff, mypy | `athena/` packages |
| Benchmarks | pytest `-m benchmark` | `athena-core` (CI `continue-on-error`) |

Integration tests (`@pytest.mark.integration`) are excluded from default pytest runs and CI unit suite.

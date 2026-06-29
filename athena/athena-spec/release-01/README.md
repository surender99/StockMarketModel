# ATH-REL-001 Core Framework — Section Index

> **Release package:** [ATH-REL-001-Core-Framework.md](../ATH-REL-001-Core-Framework.md)  
> **Source zip:** `References/ATH-REL-001-Core-Framework.zip`

This index maps the ATH-REL-001 Release-01 folder taxonomy to canonical specs and `athena-core` modules. Do not duplicate content here — follow the links.

---

## Section Map

| Section | Zip Status (v0.1) | Canonical Spec | Code / Tooling |
|---------|-------------------|----------------|----------------|
| **00 Overview** | Placeholder | [ATH-REL-001](../ATH-REL-001-Core-Framework.md) | — |
| **01 Configuration** | Placeholder | [ATH-003](../ATH-003-Repository-Architecture.md) | `application/config.py`, `core_config.py`, `config_loader.py` |
| **02 Dependency Injection** | Placeholder | [AES-0201](../architecture/AES-0201-Clean-Architecture.md) | `application/container.py`, `bootstrap.py` |
| **03 Plugin Framework** | Placeholder | [AES-0202](../architecture/AES-0202-Plugin-Architecture.md) | `domain/plugins/` |
| **04 Event Bus** | Placeholder | [ATH-REL-001](../ATH-REL-001-Core-Framework.md) | `domain/events/` |
| **05 Logging** | Placeholder | [ATH-002](../ATH-002-Engineering-Standards.md) | `infrastructure/logging.py` |
| **06 Error Handling** | Placeholder | [ATH-REL-001](../ATH-REL-001-Core-Framework.md) | `domain/errors.py` |
| **07 Core Utilities** | Placeholder | [ATH-REL-001](../ATH-REL-001-Core-Framework.md) | `domain/common/` |
| **08 Contracts** | Placeholder | [contracts/](../contracts/), `domain/ports/` | Port protocols |
| **09 Testing** | Placeholder | [ATH-002](../ATH-002-Engineering-Standards.md) | `tests/test_core_framework.py` |
| **10 Benchmarks** | Placeholder | [athena-core/benchmarks/](../../athena-core/benchmarks/README.md) | `tests/benchmarks/` |
| **11 Quality Gates** | Placeholder | [Definition of Done](../checklists/Definition-of-Done.md) | CI, pre-commit |
| **12 Playbooks** | Placeholder | [athena-docs/handbook/](../../athena-docs/handbook/) | — |

---

## REQ Traceability (Release-01)

| REQ ID | Section | Module |
|--------|---------|--------|
| REQ-CORE-CFG-001 | 01 Configuration | `application/core_config.py` |
| REQ-CORE-DI-001 | 02 Dependency Injection | `application/container.py`, `bootstrap.py` |
| REQ-CORE-PLG-001 | 03 Plugin Framework | `domain/plugins/registry.py` |
| REQ-CORE-EVT-001 | 04 Event Bus | `domain/events/bus.py` |
| REQ-CORE-LOG-001 | 05 Logging | `infrastructure/logging.py` |
| REQ-CORE-ERR-001 | 06 Error Handling | `domain/errors.py` |
| REQ-CORE-UTL-001 | 07 Core Utilities | `domain/common/` |
| REQ-CORE-CTR-001 | 08 Contracts | `domain/ports/event_publisher.py` |

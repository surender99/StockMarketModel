# ATH-REL-001 – Core Framework (Release-01)

> **Version:** v0.1  
> **Source:** `References/ATH-REL-001-Core-Framework.zip`  
> **Status:** Spec-integrated (skeleton release package)  
> **Validation:** [packages/PACKAGE-REL-001-COMPLETE.md](packages/PACKAGE-REL-001-COMPLETE.md)

ATH-REL-001 is the **foundational core framework release package** for Athena Release-01. It defines the taxonomy and implementation order for configuration, dependency injection, plugins, events, logging, errors, utilities, and shared contracts used by every `athena-core` module.

---

## Purpose

| Aspect | Detail |
|--------|--------|
| **What** | Core framework: config hierarchy, DI/bootstrap, plugin lifecycle, event bus, structured logging, error hierarchy, shared types, ports |
| **When** | Applied before extending domain engines (data, features, backtest, portfolio) |
| **Who** | `athena-core` developers, SDK/CLI integrators, AI coding agents |

Release-01 v0.1 ships as a **skeleton**: section READMEs are placeholders. Canonical, actionable content lives in existing ATH/AES documents and `athena-core` modules cross-linked from [release-01/](release-01/README.md).

---

## Relationship to ATH-REL-000 and athena-core

| ID | Role | Canonical Path |
|----|------|----------------|
| **ATH-REL-000** | Release-00 engineering standards taxonomy | [ATH-REL-000-Engineering-Standards.md](ATH-REL-000-Engineering-Standards.md) |
| **ATH-REL-001** | Release-01 core framework taxonomy | This document |
| **ATH-003** | Repository layout and Clean Architecture | [ATH-003-Repository-Architecture.md](ATH-003-Repository-Architecture.md) |
| **AES-0201** | Layer dependency rules | [architecture/AES-0201-Clean-Architecture.md](architecture/AES-0201-Clean-Architecture.md) |
| **AES-0202** | Plugin contract and registry | [architecture/AES-0202-Plugin-Architecture.md](architecture/AES-0202-Plugin-Architecture.md) |

**Reading order:** ATH-REL-000 (standards) → ATH-REL-001 (this index) → ATH-003 (repo) → AES-0201/0202 (architecture) → domain REQ.

**Implementation order (from zip Overview):** Configuration → Dependency Injection → Plugin Framework → Event Bus → Logging → Error Handling → Core Utilities → Contracts → Testing → Benchmarks.

---

## Release Package Sections (v0.1)

| # | Section | Zip Folder | Canonical Spec / Code |
|---|---------|------------|------------------------|
| 00 | Overview | `00-Overview` | This document |
| 01 | Configuration | `01-Configuration` | `athena-core/application/config.py`, `core_config.py`, `config_loader.py` |
| 02 | Dependency Injection | `02-Dependency-Injection` | `athena-core/application/container.py`, `bootstrap.py` |
| 03 | Plugin Framework | `03-Plugin-Framework` | `athena-core/domain/plugins/`, [AES-0202](architecture/AES-0202-Plugin-Architecture.md) |
| 04 | Event Bus | `04-Event-Bus` | `athena-core/domain/events/` |
| 05 | Logging | `05-Logging` | `athena-core/infrastructure/logging.py` |
| 06 | Error Handling | `06-Error-Handling` | `athena-core/domain/errors.py`, `application/errors.py` (ingest) |
| 07 | Core Utilities | `07-Core-Utilities` | `athena-core/domain/common/` |
| 08 | Contracts | `08-Contracts` | `athena-core/domain/ports/`, [contracts/](contracts/) |
| 09 | Testing | `09-Testing` | [ATH-002](ATH-002-Engineering-Standards.md), `athena-core/tests/` |
| 10 | Benchmarks | `10-Benchmarks` | [athena-core/benchmarks/](../athena-core/benchmarks/README.md) |
| 11 | Quality Gates | `11-Quality-Gates` | CI, pre-commit, [Definition of Done](checklists/Definition-of-Done.md) |
| 12 | Implementation Playbooks | `12-Implementation-Playbooks` | [athena-docs/handbook/](../athena-docs/handbook/), [AES-0006](governance/AES-0006-AI-Coding-Standards.md) |

Full section index: [release-01/README.md](release-01/README.md).

---

## Implemented vs Documented-Only (v0.1)

| Category | Status | Evidence |
|----------|--------|----------|
| Configuration hierarchy & profiles | ✅ Implemented | `AthenaConfig`, `CoreFrameworkConfig`, `config_loader.py` |
| DI container & bootstrap | ✅ Implemented | `ServiceContainer`, `bootstrap_athena_core`, `CoreContext` |
| Plugin registry lifecycle | ✅ Implemented | `PluginRegistry`, `PluginLifecycle`, `AthenaRuntime.plugin_registry` |
| Event bus (sync) | ✅ Implemented | `EventBus`, `DomainEvent`, `EventPublisherPort` |
| Structured logging + correlation ID | ✅ Implemented | `configure_logging`, `correlation_scope` |
| Domain error hierarchy | ✅ Implemented | `AthenaError`, `ErrorCode` |
| Core utilities (types, serialization, time) | ✅ Implemented | `domain/common/` |
| Core ports | ✅ Implemented | `domain/ports/` including `EventPublisherPort` |
| Runtime composition root | ✅ Implemented | `AthenaRuntime` wires `bootstrap_athena_core` |
| Async event dispatch | 📋 Documented-only | Deferred — sync bus sufficient for v0.1 |
| Plugin auto-discovery from entry points | 📋 Documented-only | `discover()` accepts iterables; setuptools entry points deferred |
| Section placeholder READMEs in zip | 📋 Skeleton only | Mapped to canonical paths above |
| `ATH-REL-001-Core-Framework-Overview.docx` | 📋 Binary only | Section list captured in this document |

---

## Related Documents

- [ATH-REL-000 Engineering Standards](ATH-REL-000-Engineering-Standards.md)
- [ATH-003 Repository Architecture](ATH-003-Repository-Architecture.md)
- [REFERENCES-INDEX](REFERENCES-INDEX.md)
- [REFERENCES-INTEGRATION-COMPLETE](REFERENCES-INTEGRATION-COMPLETE.md)

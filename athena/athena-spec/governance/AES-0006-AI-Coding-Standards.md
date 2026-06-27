# AES-0006 – AI Coding Standards

> **References source:** `References/Athena-Package-01-Governance/standards/AES-0006-AI-Coding-Standards.md`  
> **Complements:** [ATH-002 Engineering Standards](../ATH-002-Engineering-Standards.md)

Rules for human developers and AI coding agents implementing Athena modules.

---

## Mandatory Workflow

1. **Read Constitution** — [ATH-000](../ATH-000-Philosophy.md) / [AES-0001](AES-0001-Constitution.md)
2. **Read Requirement** — relevant `REQ-*` in [requirements/](../requirements/)
3. **Read Contract** — provider interface when integrating a References package (e.g. `DataProvider`, `StrategyProvider`)
4. **Implement requested scope only** — no drive-by refactors or speculative features
5. **Generate tests** — unit tests required; integration tests when I/O or network involved
6. **Generate documentation** — update spec or module docstrings when behavior changes
7. **Stop** — do not expand scope without an approved REQ or RFC

---

## Implementation Rules

| Rule | Detail |
|------|--------|
| **No hardcoded strategy logic** | Strategies are YAML + validated config, not embedded Python branches |
| **Configuration over hardcoding** | Paths, thresholds, universes, and costs live in YAML or env |
| **REQ traceability** | Reference REQ IDs in commits, tests, and module docstrings where applicable |
| **Typed Python** | Python 3.11+ with type hints on public APIs |
| **Clean Architecture** | Domain has no I/O; infrastructure implements ports ([ATH-003](../ATH-003-Repository-Architecture.md)) |
| **Plugin-ready** | New indicators, data sources, and strategies via providers — not monolith edits |
| **Quant compliance** | Follow [AES-0005 Quant Standards](AES-0005-Quant-Standards.md) for any research code |

---

## Agent Prompt (Canonical)

Use this when delegating implementation to an AI agent:

```
Read:
- ATH-000 / AES-0001 (Constitution)
- The target REQ-* specification
- The relevant provider contract (if any)
- ATH-002 / AES-0006 (Engineering & AI standards)
- AES-0005 (Quant standards) when touching backtest, features, or ML

Implement only the requested module and acceptance criteria.
Add unit tests. Update documentation if behavior changes.
Stop when acceptance criteria are met — do not expand scope.
```

Full prompt template: [prompts/AI-Implementation-Prompt.md](../prompts/AI-Implementation-Prompt.md).

---

## Definition of Done

An AI-assisted change is complete only when [checklists/Definition-of-Done.md](../checklists/Definition-of-Done.md) is satisfied.

---

## Related Documents

- [ATH-002 Engineering Standards](../ATH-002-Engineering-Standards.md)
- [ATH-004 Requirement Standard](../ATH-004-Requirement-Standard.md)
- [prompts/AI-Implementation-Prompt.md](../prompts/AI-Implementation-Prompt.md)

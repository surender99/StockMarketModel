# AI Implementation Prompt

> **References source:** `References/Athena-Package-01-Governance/prompts/AI-Implementation-Prompt.md`  
> **Standards:** [AES-0006 AI Coding Standards](../governance/AES-0006-AI-Coding-Standards.md)

Use this prompt when delegating a bounded implementation task to an AI coding agent.

---

## Prompt Template

```
You are implementing a module for Athena — an AI-native Quantitative Research Operating System.

## Read first (mandatory)

1. Constitution: athena/athena-spec/ATH-000-Philosophy.md (or governance/AES-0001-Constitution.md)
2. Requirement: athena/athena-spec/requirements/<REQ-ID>.md
3. Contract: (if applicable) provider interface from References package or athena-spec
4. Engineering: athena/athena-spec/ATH-002-Engineering-Standards.md
5. AI workflow: athena/athena-spec/governance/AES-0006-AI-Coding-Standards.md
6. Quant rules: athena/athena-spec/governance/AES-0005-Quant-Standards.md (backtest, features, ML)

## Task

Implement only: <MODULE / REQ-ID / acceptance criteria>.

## Constraints

- Match existing code style and Clean Architecture layers (ATH-003).
- Configuration over hardcoding; reference REQ IDs in tests.
- Add unit tests; integration tests only if REQ requires I/O.
- Update documentation only where behavior changes.
- Do not expand scope beyond the REQ.

## Stop condition

When acceptance criteria pass and Definition of Done (checklists/Definition-of-Done.md) is met.
```

---

## Related Documents

- [AES-0006 AI Coding Standards](../governance/AES-0006-AI-Coding-Standards.md)
- [templates/Requirement-Template.md](../templates/Requirement-Template.md)

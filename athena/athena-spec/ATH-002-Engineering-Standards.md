# ATH-002 – Engineering Standards

> **Release package:** [ATH-REL-000 Engineering Standards](ATH-REL-000-Engineering-Standards.md) (Release-00 v0.1)
> **AI agent workflow:** [governance/AES-0006-AI-Coding-Standards.md](governance/AES-0006-AI-Coding-Standards.md)
> **Quant research rules:** [governance/AES-0005-Quant-Standards.md](governance/AES-0005-Quant-Standards.md)
> **Section index:** [engineering-standards/README.md](engineering-standards/README.md)

## Architecture
- Clean Architecture
- SOLID
- Dependency Injection
- Plugin-based design

## Coding
- Python 3.11+
- Type hints (mypy strict on `athena-core`)
- ruff lint and format
- Structured logging
- Configuration driven

## Testing
- Unit tests required for all modules
- Integration tests — mark `@pytest.mark.integration` for network/live data
- Benchmark tests — mark `@pytest.mark.benchmark` (optional in CI)
- Default pytest excludes integration and benchmark markers

## Quality Gates
- Pre-commit: trailing whitespace, yaml check, ruff, mypy (`athena-core`)
- CI: full pytest, coverage (`athena-core`), ruff check/format, mypy, pre-commit
- Definition of Done: [checklists/Definition-of-Done.md](checklists/Definition-of-Done.md)

## AI Coding Rules
- Never hardcode strategy logic
- Everything configurable
- Tests required
- Requirement IDs referenced in code
- Implement requested scope only — see [AES-0006](governance/AES-0006-AI-Coding-Standards.md)

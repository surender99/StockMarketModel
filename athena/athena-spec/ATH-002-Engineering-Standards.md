# ATH-002 – Engineering Standards

> **AI agent workflow:** [governance/AES-0006-AI-Coding-Standards.md](governance/AES-0006-AI-Coding-Standards.md)  
> **Quant research rules:** [governance/AES-0005-Quant-Standards.md](governance/AES-0005-Quant-Standards.md)

## Architecture
- Clean Architecture
- SOLID
- Dependency Injection
- Plugin-based design

## Coding
- Python 3.12+
- Type hints
- Unit tests
- Integration tests (mark `@pytest.mark.integration` for network/live data)
- Structured logging
- Configuration driven

## AI Coding Rules
- Never hardcode strategy logic
- Everything configurable
- Tests required
- Requirement IDs referenced in code
- Implement requested scope only — see [AES-0006](governance/AES-0006-AI-Coding-Standards.md)

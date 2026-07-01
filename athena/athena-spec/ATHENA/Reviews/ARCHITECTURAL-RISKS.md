# Architectural Risks

> **Status:** Living document — review quarterly

## Identified risks

| Risk | Mitigation |
|------|------------|
| **Module explosion** | Facade-first extraction (ADR-0006); rich manifests (ADR-0007) |
| **Codegen discipline** | `CODEGEN-STANDARD.md` — never edit generated files; CI event compatibility tests |
| **Plugin compatibility** | Versioned event schemas; `BrokerPlugin` protocol in `athena-brokers` |
| **Dependency drift** | `check_dependencies.py` + architecture fitness tests in `make test` |

## Monitoring

- `make graph` regenerates BUILD-GRAPH.md
- `athena_inspector.py --graph` for manifest-derived snippets

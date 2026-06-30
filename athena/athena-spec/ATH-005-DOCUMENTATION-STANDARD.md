# ATH-005 — Documentation Standard

> **Status:** Accepted  
> **Applies to:** All Athena features, APS implementations, and packages

## Required Artifacts per Feature

Every feature or APS implementation must include:

| Artifact | Location | Required |
|----------|----------|----------|
| **README** | Package or module root | Yes |
| **Architecture** | ADR or APS architecture section | Yes for new subsystems |
| **Interfaces** | `athena-spec/interfaces/INTERFACE-CATALOG.md` | Yes for public APIs |
| **Events** | `athena-spec/events/EVENT-CATALOG.md` | Yes if feature publishes/subscribes |
| **Tests** | `*/tests/` with pytest | Yes |
| **Examples** | APS **Example** field, notebook, or CLI | Yes for user-facing features |
| **Prompt** | `athena-spec/ATHENA/Prompts/` | For AI-assisted development |
| **Status** | APS traceability **Status** field | Yes |

## APS Traceability

All APS markdown files use [_TEMPLATE.md](ATHENA/APS/_TEMPLATE.md) with required fields:

- APS ID, Implemented In, Tests, Benchmarks, Owner, Status, Release, Example

## Package README Minimum

```markdown
# package-name
## Purpose
## Install
## Modules
## Tests
## Dependencies
```

## Statistics Independence

Analytics and statistics documentation belongs under `domain/analytics` and `domain/statistics`, not under indicators. Cross-reference in APS dependencies only.

## References

- [ATH-004 Requirement Standard](ATH-004-Requirement-Standard.md)
- [ADR-0005 athena-os](adrs/ADR-0005-athena-os.md)
- [TRACEABILITY-INDEX.md](ATHENA/APS/TRACEABILITY-INDEX.md)

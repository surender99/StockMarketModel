# Codegen Standard

> **Rule:** NEVER manually edit generated code.

## Generated artifacts

| Generator | Output | Source |
|-----------|--------|--------|
| `generate_events.py` | `athena-common/.../events_generated.py` | `athena-spec/events/registry/*.event.yaml` |
| `generate_dtos.py` | `athena-common/.../dtos_generated.py` | `athena-spec/schemas/dtos/*.dto.yaml` |
| `generate_openapi.py` | `athena-spec/metadata/generated/openapi-stub.yaml` | module `api` sections (stub) |
| `generate_proto.py` | `athena-spec/metadata/generated/athena.proto` | interface catalog (stub) |
| `generate_clients.py` | `athena-sdk/.../clients_generated.py` | OpenAPI (stub) |
| `generate_docs.py` | `athena-spec/metadata/generated/MODULE-INDEX.md` | `athena-*/module.yaml` |
| `generate_manifests.py` | `athena-spec/metadata/generated/manifests/` | component metadata YAML |

## Regeneration

```bash
cd athena && make codegen
```

All generated files are marked with:

```
# GENERATED — DO NOT EDIT
```

## CI

- Architecture tests validate event YAML ↔ generated Python parity.
- PRs that change registry YAML must include regenerated outputs.

## References

- [ADR-0007](../adrs/ADR-0007-rich-module-manifests.md)
- [EVENT-REGISTRY-STANDARD.md](../events/EVENT-REGISTRY-STANDARD.md)

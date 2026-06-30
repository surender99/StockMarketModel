# athena-testing

Testing infrastructure for the Athena platform: golden datasets, fixtures, performance benchmarks, and chaos test stubs.

## Layout

```
athena-testing/
  golden-datasets/   → see README (canonical fixtures in athena-spec)
  fixtures/          → test-local fixtures
  performance/       → performance test helpers
  chaos/             → chaos/resilience stubs
  benchmarks/        → performance gate benchmarks
  tests/             → smoke and integration tests
```

## Golden Datasets

Canonical golden datasets live in `athena-spec/ATHENA/Golden-Datasets/`. This package includes:

- `golden-datasets/README.md` — pointer to spec fixtures
- `fixtures/` — copies or generated samples for CI

APS validation requirements are tracked in [TRACEABILITY-INDEX.md](../athena-spec/ATHENA/APS/TRACEABILITY-INDEX.md).

## Install

```bash
pip install -e "../athena-os"
pip install -e "../athena-core[dev]"
pip install -e ".[dev]"
```

## Run Tests

```bash
pytest
```

## Performance Gates

See [PERFORMANCE-GATES.md](../athena-spec/ATHENA/Benchmarks/PERFORMANCE-GATES.md).

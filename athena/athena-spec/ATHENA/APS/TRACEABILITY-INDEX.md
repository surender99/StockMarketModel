# APS Traceability Index

> **Purpose:** Map APS IDs to implementation paths, tests, and benchmarks.  
> **Validation:** Golden datasets in [Golden-Datasets/](../Golden-Datasets/README.md) linked per APS where applicable.  
> **Testing package:** [athena-testing](../../../athena-testing/README.md)

## Traceability Fields (required per APS)

Every APS markdown file must include the traceability block from [_TEMPLATE.md](_TEMPLATE.md):

| Field | Description |
|-------|-------------|
| APS ID | Canonical identifier |
| Implemented In | Source code path(s) |
| Tests | Pytest module(s) |
| Benchmarks | Performance test path or N/A |
| Owner | Responsible team/person |
| Status | Draft / MVP / Partial / Complete / Deferred |
| Release | REL package |
| Example | Runnable example or golden dataset |

---

## MVP APS — Code Traceability

### Foundation (athena-os)

| APS ID | Implemented In | Tests | Benchmarks | Status | Release |
|--------|----------------|-------|------------|--------|---------|
| APS-004 | `athena-os/src/athena_os/event_bus.py` | `athena-os/tests/test_athena_os.py` | N/A | MVP | REL-001 |
| APS-003 | `athena-os/src/athena_os/plugins.py` | `athena-os/tests/test_athena_os.py`, `athena-core/tests/test_plugin_registry.py` | N/A | MVP | REL-001 |
| APS-001 | `athena-os/src/athena_os/configuration.py` | `athena-os/tests/test_athena_os.py` | N/A | MVP | REL-001 |
| APS-005 | `athena-os/src/athena_os/registry.py` | `athena-os/tests/test_athena_os.py` | N/A | MVP | REL-001 |

### Indicators

| APS ID | Implemented In | Tests | Benchmarks | Status | Release |
|--------|----------------|-------|------------|--------|---------|
| APS-IND-ADX-001 | `athena-core/.../indicators/adx.py` | `test_indicator_aps.py` | `athena-testing/benchmarks/` | MVP | REL-004 |
| APS-IND-EMA-001 | `athena-core/.../indicators/ema.py` | `test_indicators_ema.py` | `athena-testing/benchmarks/` | MVP | REL-004 |
| APS-IND-RSI-001 | `athena-core/.../indicators/rsi.py` | `test_indicator_framework.py` | `athena-testing/benchmarks/` | MVP | REL-004 |
| APS-IND-BENCH-100K-001 | `athena-core/.../indicators/` | `test_indicator_benchmarks.py` | `athena-testing/benchmarks/test_indicator_throughput.py` | MVP | REL-004 |

### Patterns

| APS ID | Implemented In | Tests | Benchmarks | Status | Release |
|--------|----------------|-------|------------|--------|---------|
| APS-PAT-CS-HAMMER-001 | `athena-core/.../patterns/candlestick.py` | `test_pattern_aps.py` | N/A | MVP | REL-005 |
| APS-PAT-PIPELINE-001 | `athena-core/.../patterns/pipeline.py` | `test_pattern_architecture.py` | N/A | Partial | REL-005 |

### Strategies

| APS ID | Implemented In | Tests | Benchmarks | Status | Release |
|--------|----------------|-------|------------|--------|---------|
| APS-SIGNAL-CORE-001 | `athena-core/.../strategy/signals.py` | `test_strategy_aps.py` | N/A | MVP | REL-006 |
| APS-DSL-EXECUTOR-001 | `athena-core/.../strategy/dsl_executor.py` | `test_strategy_dsl.py` | N/A | MVP | REL-006 |

### Simulation

| APS ID | Implemented In | Tests | Benchmarks | Status | Release |
|--------|----------------|-------|------------|--------|---------|
| APS-SIM-SESSION-001 | `athena-core/.../simulation/session.py` | `test_phase6_simulation.py` | N/A | MVP | REL-007 |
| APS-EXEC-TRAILING-001 | `athena-core/.../simulation/trailing_stops.py` | `test_phase6_simulation.py` | N/A | MVP | REL-007 |

### Portfolio Intelligence

| APS ID | Implemented In | Tests | Benchmarks | Status | Release |
|--------|----------------|-------|------------|--------|---------|
| APS-CORR-CORE-001 | `athena-core/.../portfolio_intelligence/correlation.py` | `test_phase678_aps.py` | N/A | MVP | REL-008 |

### Quantitative Analytics

| APS ID | Implemented In | Tests | Benchmarks | Status | Release |
|--------|----------------|-------|------------|--------|---------|
| APS-HYP-KS-001 | `athena-core/.../analytics/hypothesis.py` | `test_analytics_aps.py` | N/A | MVP | REL-009 |
| APS-CORR-SPEARMAN-001 | `athena-core/.../analytics/correlation.py` | `test_analytics_aps.py` | N/A | MVP | REL-009 |

### Research & Experimentation

| APS ID | Implemented In | Tests | Benchmarks | Status | Release |
|--------|----------------|-------|------------|--------|---------|
| APS-RES-PROJECT-001 | `athena-core/.../research/projects.py` | `test_qrep_aps.py` | N/A | MVP | REL-010 |
| APS-REPRO-BUNDLE-001 | `athena-core/.../research/reproducibility.py` | `test_qrep_aps.py` | N/A | MVP | REL-010 |

---

## Golden Dataset Validation

APS implementations that accept OHLCV or structured inputs should reference a fixture from:

- `athena-spec/ATHENA/Golden-Datasets/`
- `athena-testing/golden-datasets/` (symlink/README to spec fixtures)

Run validation via `athena-testing` smoke tests after adding new golden datasets.

---

## Maintenance

1. Add a row when an APS gains code implementation.
2. Update **Status** in both the APS file and this index.
3. Link new events to [events/EVENT-CATALOG.md](../../events/EVENT-CATALOG.md).
4. Link new public APIs to [interfaces/INTERFACE-CATALOG.md](../../interfaces/INTERFACE-CATALOG.md).

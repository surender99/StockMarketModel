# Production Readiness Checklist

> **Use before:** REL production sign-off, deployment to live environments.

## Infrastructure

- [ ] `athena-os` runtime bootstrap verified
- [ ] Configuration secrets loaded via `SecretsVault` (not plaintext in prod)
- [ ] Structured logging with correlation IDs enabled (`json_logs=true`)
- [ ] Metrics collector wired to observability backend (stub → production)

## Resilience

- [ ] Chaos tests defined in `athena-testing/chaos/` (stubs acceptable for MVP)
- [ ] Event bus handler failure policy documented
- [ ] Simulation replay determinism verified

## Operations

- [ ] Runbooks for ingest failure, backtest OOM, research experiment stuck
- [ ] Incident response: severity levels, on-call rotation
- [ ] Rollback procedure for core and SDK releases

## Security

- [ ] RBAC roles configured (admin, researcher, operator, viewer)
- [ ] Audit trail enabled for sensitive operations
- [ ] Dependency check passes: `python athena/scripts/check_dependencies.py`

## Data

- [ ] Golden dataset validation linked in TRACEABILITY-INDEX
- [ ] Data lineage captured for research experiments

## Sign-off

| Role | Name | Date |
|------|------|------|
| Engineering | | |
| Quant | | |
| Security | | |

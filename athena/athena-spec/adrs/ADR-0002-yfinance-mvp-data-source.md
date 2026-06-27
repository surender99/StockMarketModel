# ADR-0002 – yfinance as MVP Market Data Source

> **Status:** Accepted  
> **Date:** 2026-06-27  
> **Deciders:** Athena platform architects

## Context

The MVP requires daily OHLCV for NSE-listed symbols (`.NS` suffix) without broker integration or paid data contracts. Researchers need a zero-cost path to ingest, backtest, and validate strategies before committing to production-grade vendors.

## Decision

Use **yfinance** as the MVP market data source for daily OHLCV ingest.

## Alternatives Considered

| Option | Pros | Cons |
|--------|------|------|
| **yfinance** (chosen) | Free; no API keys; works for `.NS` symbols; fast MVP bootstrap | Unofficial; no guaranteed SLA; limited corporate-action handling; rate limits |
| **NSE official / exchange APIs** | Authoritative prices; regulatory alignment | Licensing, registration, and integration effort exceed MVP timeline |
| **Paid vendors (e.g. Bloomberg, Refinitiv, Indian data vendors)** | Adjusted data; corporate actions; support | Cost; contract negotiation; not suitable for open research MVP |
| **Manual CSV uploads only** | Full control | Poor researcher UX; blocks automated ingest workflows |

## Consequences

- **Positive:** Enables end-to-end ingest → backtest loop on day one; integration tests can be gated behind `@pytest.mark.integration`.
- **Negative:** Data quality disclaimers required; no split/dividend adjustment in MVP; production trading must not rely on yfinance alone.
- **Neutral:** `DataProvider` port allows swapping to NSE official or vendor feeds without changing domain logic.

## Compliance

- [x] [ATH-003 Repository Architecture](../ATH-003-Repository-Architecture.md) layers respected
- [x] [AES-0005 Quant Standards](../governance/AES-0005-Quant-Standards.md) (if research-impacting)
- [ ] Related REQ or RFC linked below

## References

- REQ-DATA-INGEST-001
- `athena_core.infrastructure.yfinance_client`
- PLATFORM-COMPLETE.md — Known Limitations (market data)

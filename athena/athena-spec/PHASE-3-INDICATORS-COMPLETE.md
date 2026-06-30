# Phase 3 — Indicators APS Complete (Expanded Architecture)

**Validated by:** Master Orchestrator Agent  
**Date:** 2026-06-30  
**Repository:** StockMarketModel (`athena/` monorepo)  
**Source:** `References/PHASE 3 Architecture.docx` (new) + `References/ATH-REL-004-Indicator-Framework.zip`  
**Structure:** [ATHENA/APS/Indicators/](ATHENA/APS/Indicators/README.md)

---

## Executive Summary

Phase 3 Indicators expanded from 25 to **102 APS specifications** across **16 domains**, driven by the new `PHASE 3 Architecture.docx` reference. MVP wiring adds price transforms, indicator pipeline, metadata store, and a full deferred-indicator catalog (77 entries). Existing 15 builtin indicators remain MVP.

**Status: COMPLETE** (specs + MVP extensions)

---

## Source Documents

| Item | Value |
|------|-------|
| **New file** | `References/PHASE 3 Architecture.docx` (2026-06-30) |
| **Prior source** | `References/ATH-REL-004-Indicator-Framework.zip` |
| **APS count** | 102 specs across 16 domains |
| **REL index** | [ATH-REL-004-Indicator-Framework.md](ATH-REL-004-Indicator-Framework.md) |

---

## Indicators APS Domains

| # | Domain | APS count | Index |
|---|--------|-----------|-------|
| 1 | Indicator Architecture | 1 | [Indicator-Architecture/](ATHENA/APS/Indicators/Indicator-Architecture/README.md) |
| 2 | Indicator Engine | 6 | [Indicator-Engine/](ATHENA/APS/Indicators/Indicator-Engine/README.md) |
| 3 | Indicator Registry | 3 | [Indicator-Registry/](ATHENA/APS/Indicators/Indicator-Registry/README.md) |
| 4 | Price Transformations | 9 | [Price-Transformations/](ATHENA/APS/Indicators/Price-Transformations/README.md) |
| 5 | Moving Averages | 12 | [Moving-Averages/](ATHENA/APS/Indicators/Moving-Averages/README.md) |
| 6 | Trend Indicators | 10 | [Trend-Indicators/](ATHENA/APS/Indicators/Trend-Indicators/README.md) |
| 7 | Momentum Indicators | 8 | [Momentum-Indicators/](ATHENA/APS/Indicators/Momentum-Indicators/README.md) |
| 8 | Oscillators | 7 | [Oscillators/](ATHENA/APS/Indicators/Oscillators/README.md) |
| 9 | Volatility Indicators | 7 | [Volatility-Indicators/](ATHENA/APS/Indicators/Volatility-Indicators/README.md) |
| 10 | Volume Indicators | 9 | [Volume-Indicators/](ATHENA/APS/Indicators/Volume-Indicators/README.md) |
| 11 | Market Breadth | 7 | [Market-Breadth/](ATHENA/APS/Indicators/Market-Breadth/README.md) |
| 12 | Cycle Indicators | 4 | [Cycle-Indicators/](ATHENA/APS/Indicators/Cycle-Indicators/README.md) |
| 13 | Composite Indicators | 7 | [Composite-Indicators/](ATHENA/APS/Indicators/Composite-Indicators/README.md) |
| 14 | Indicator Validation | 2 | [Indicator-Validation/](ATHENA/APS/Indicators/Indicator-Validation/README.md) |
| 15 | Indicator Testing | 5 | [Indicator-Testing/](ATHENA/APS/Indicators/Indicator-Testing/README.md) |
| 16 | Indicator Benchmarking | 5 | [Indicator-Benchmarking/](ATHENA/APS/Indicators/Indicator-Benchmarking/README.md) |

**Spec path:** [ATHENA/APS/Indicators/](ATHENA/APS/Indicators/README.md)

---

## athena-core Extensions (Phase 3 Architecture)

| Module | APS | Change |
|--------|-----|--------|
| `domain/indicators/catalog.py` | APS-IND-REGISTRY-001 | Expanded — 80 catalog entries (19 MVP, 1 Partial, 60 Deferred) |
| `domain/indicators/price_transforms.py` | APS-PRICE-HLC3/HL2/OHLC4/MEDIANPRICE-001 | New — vectorized price transforms |
| `domain/indicators/pipeline.py` | APS-IND-PIPELINE-001 | New — chained indicator pipeline |
| `domain/indicators/metadata.py` | APS-IND-METADATA-001 | New — metadata store |
| `tests/test_indicator_architecture.py` | — | +6 tests |
| `tests/test_indicator_aps.py` | — | Updated MVP count (19) |

---

## Golden Datasets

| Fixture | Path |
|---------|------|
| 30-day OHLCV | [ATHENA/Golden-Datasets/ohlcv-sample-30d.csv](ATHENA/Golden-Datasets/ohlcv-sample-30d.csv) |

---

## Schemas

| Schema | Path |
|--------|------|
| Indicator metadata | [ATHENA/Schemas/indicator-metadata.json](ATHENA/Schemas/indicator-metadata.json) |

---

## Benchmarks

[ATHENA/Benchmarks/indicators.md](ATHENA/Benchmarks/indicators.md) — 10K bar targets + deferred scale targets.

---

## Acceptance Gate

- [x] New source document located (`PHASE 3 Architecture.docx`)
- [x] 102 Indicators APS specs with REQ IDs and ATH-004 acceptance criteria
- [x] APS wired to `athena-core` module paths (MVP / Partial / Deferred per spec)
- [x] Expanded indicator catalog, price transforms, pipeline, metadata store
- [x] Indicator metadata schema updated with new categories
- [x] Indicator benchmarks documented (incl. cross-library tolerance)
- [x] Unit tests for new MVP modules
- [x] Navigation updated (`ATHENA/APS/Indicators/README.md`)

---

## Phase 3 Indicators Status

**COMPLETE** — Expanded architecture specs, catalog, price transforms, pipeline, metadata, and tests implemented. Deferred indicators (Ichimoku, VWAP, cycle/composite, etc.) have published APS specs awaiting formula implementation.

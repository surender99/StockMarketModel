# Indicators APS — Phase 3

Implementation specifications from **ATH-REL-004-Indicator-Framework.md** and **`References/PHASE 3 Architecture.docx`** (expanded architecture).

**Validation:** [PHASE-3-INDICATORS-COMPLETE.md](../../PHASE-3-INDICATORS-COMPLETE.md)

## Domains

| Domain | Index | APS count |
|--------|-------|-----------|
| **Indicator Architecture** | [Indicator-Architecture/](Indicator-Architecture/README.md) | 1 |
| **Indicator Engine** | [Indicator-Engine/](Indicator-Engine/README.md) | 6 |
| **Indicator Registry** | [Indicator-Registry/](Indicator-Registry/README.md) | 3 |
| **Price Transformations** | [Price-Transformations/](Price-Transformations/README.md) | 9 |
| **Moving Averages** | [Moving-Averages/](Moving-Averages/README.md) | 12 |
| **Trend Indicators** | [Trend-Indicators/](Trend-Indicators/README.md) | 10 |
| **Momentum Indicators** | [Momentum-Indicators/](Momentum-Indicators/README.md) | 8 |
| **Oscillators** | [Oscillators/](Oscillators/README.md) | 7 |
| **Volatility Indicators** | [Volatility-Indicators/](Volatility-Indicators/README.md) | 7 |
| **Volume Indicators** | [Volume-Indicators/](Volume-Indicators/README.md) | 9 |
| **Market Breadth** | [Market-Breadth/](Market-Breadth/README.md) | 7 |
| **Cycle Indicators** | [Cycle-Indicators/](Cycle-Indicators/README.md) | 4 |
| **Composite Indicators** | [Composite-Indicators/](Composite-Indicators/README.md) | 7 |
| **Indicator Validation** | [Indicator-Validation/](Indicator-Validation/README.md) | 2 |
| **Indicator Testing** | [Indicator-Testing/](Indicator-Testing/README.md) | 5 |
| **Indicator Benchmarking** | [Indicator-Benchmarking/](Indicator-Benchmarking/README.md) | 5 |

**Total APS:** 102

## Architecture Layers (CTO Recommendation)

| Layer | Responsibility |
|-------|----------------|
| `formulas/` | Pure mathematical implementations |
| `execution/` | Batch, streaming, pipeline engines |
| `registry/` | Discovery, metadata, versioning |
| `validation/` | Cross-library reference validation |
| `benchmarks/` | Performance testing |
| `adapters/` | Pandas, Polars, Arrow interfaces |

## Related

- [ATH-REL-004-Indicator-Framework.md](../../ATH-REL-004-Indicator-Framework.md)
- [Foundation APS](../Foundation/README.md) — Phase 1 prerequisite
- [Data APS](../Data/README.md) — Phase 2 prerequisite

# AES-0005 – Quant Standards

> **References source:** `References/Athena-Package-01-Governance/standards/AES-0005-Quant-Standards.md`  
> **Complements:** [ATH-000 Philosophy](../ATH-000-Philosophy.md), [ATH-001 Vision](../ATH-001-Vision-PRD.md)

Quantitative research in Athena must be **scientifically defensible**. These rules apply to every backtest, walk-forward run, optimizer sweep, ML training set, and scanner ranking.

---

## Research Integrity

| Rule | Requirement |
|------|-------------|
| **No look-ahead bias** | Features, signals, and parameters may use only data available at or before the decision bar. No future bars, revised fundamentals, or point-in-time violations. |
| **No survivorship bias** | Universe definitions must reflect constituents as-of each rebalance or scan date. Document delisted symbols and exclusion rationale. |
| **Transaction costs** | Every backtest and walk-forward report must include configurable commission and fees (see `backtest.yaml`). |
| **Slippage** | Model fill price must apply slippage (bps or absolute) relative to the signal bar close unless a documented execution model says otherwise. |
| **Walk-forward validation** | In-sample optimization alone is insufficient. Promote strategies only after out-of-sample or walk-forward evaluation ([REQ-WALK-FORWARD-001](../requirements/REQ-WALK-FORWARD-001.md)). |
| **Benchmark vs Buy & Hold** | Report strategy metrics alongside a defined benchmark (e.g. NIFTY 50/500 buy-and-hold on the same calendar). |
| **Report failures** | Negative results, rejected hypotheses, and failed experiments must be logged in experiment tracking — not discarded. |

---

## Implementation Mapping (Athena MVP)

| Standard | Implementation |
|----------|----------------|
| Look-ahead | Bar-close signals; feature store keyed by `as_of` date; walk-forward train/test windows |
| Costs & slippage | `BacktestConfig` in strategy/backtest YAML |
| Walk-forward | `athena walk-forward`, `WalkForwardValidator` |
| Benchmark | Backtest metrics vs buy-and-hold in engine output |
| Failure reporting | `ExperimentTracker`, `compare-experiments` |

---

## Review Checklist

Before marking a research deliverable complete:

- [ ] Train and test periods are disjoint and documented
- [ ] Parameter search used only in-sample folds
- [ ] Costs and slippage match the stated execution assumption
- [ ] Benchmark and strategy use aligned calendars (NSE holidays)
- [ ] Experiment ID, git commit, and config hash are recorded
- [ ] Null or weak results are archived, not hidden

---

## Related Documents

- [AES-0001 Constitution](AES-0001-Constitution.md)
- [ATH-004 Requirement Standard](../ATH-004-Requirement-Standard.md)
- [REQ-BT-ENGINE-001](../requirements/REQ-BT-ENGINE-001.md)
- [REQ-WALK-FORWARD-001](../requirements/REQ-WALK-FORWARD-001.md)
- [checklists/Definition-of-Done.md](../checklists/Definition-of-Done.md)

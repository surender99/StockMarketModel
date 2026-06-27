# REQ-OPT-001

**Requirement ID:** REQ-OPT-001

**Title:** Strategy Parameter Optimizer

**Purpose:** Search strategy configuration parameters using walk-forward out-of-sample evaluation with multi-objective scoring.

**Description:** The optimizer evaluates grid, random, or Bayesian parameter search trials over walk-forward test folds. Each trial applies dot-path overrides to `StrategyConfig`, runs `WalkForwardValidator`, and ranks trials by a weighted composite of Sharpe ratio, max drawdown, and profit factor (configurable).

**Inputs:**
- Base `StrategyConfig` and parameter search space
- Backtest and walk-forward configuration
- Symbol universe and date range

**Outputs:**
- Ranked list of `OptimizerTrial` (parameters, aggregate metrics, composite score)
- Best trial recommendation

**Configuration:**
```yaml
optimizer:
  method: grid  # grid | random | bayesian
  max_trials: 50
  random_seed: 42
  parameters:
    - path: risk.stop_loss_pct
      type: choice
      values: [0.03, 0.05, 0.07]
    - path: indicators.ema_fast.params.period
      type: int
      min: 20
      max: 60
      step: 10
  objectives:
    - sharpe
    - max_drawdown
    - profit_factor
  objective_weights:
    sharpe: 0.4
    max_drawdown: 0.3
    profit_factor: 0.3
```

**Algorithm:**
1. Generate parameter combinations per search method.
2. Apply overrides via `apply_strategy_overrides`.
3. Run walk-forward validation on each trial.
4. Compute weighted composite score from aggregate fold metrics.
5. Return trials sorted by composite score descending.

**Dependencies:**
- REQ-WALK-FORWARD-001, REQ-STRAT-CONFIG-001, REQ-BT-ENGINE-001

**Acceptance Criteria:**
- [ ] Grid search enumerates all parameter combinations
- [ ] Random search respects `max_trials`
- [ ] Bayesian method runs sequential refinement trials
- [ ] Multi-objective composite uses Sharpe, drawdown, profit factor
- [ ] Strategy config dot-path overrides applied correctly
- [ ] CLI `optimize` command integrated

**Unit Tests:**
- Strategy override application
- Grid/random/Bayesian trial counts
- Best trial selection

**Future Enhancements:**
- Pareto frontier visualization
- Optuna integration for advanced Bayesian search

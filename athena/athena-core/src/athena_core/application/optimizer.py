"""Strategy parameter optimizer on walk-forward folds — REQ-OPT-001."""

from __future__ import annotations

import itertools
import random
from dataclasses import dataclass, field
from datetime import date
from typing import Any

import structlog

from athena_core.application.backtest_config import BacktestConfig
from athena_core.application.optimizer_config import OptimizerConfig, ParameterSpec
from athena_core.application.strategy_overrides import apply_strategy_overrides
from athena_core.application.walk_forward import WalkForwardValidator
from athena_core.domain.strategy.config import StrategyConfig

log = structlog.get_logger(__name__)

OBJECTIVE_DIRECTION: dict[str, str] = {
    "sharpe": "maximize",
    "profit_factor": "maximize",
    "total_return": "maximize",
    "cagr": "maximize",
    "win_rate": "maximize",
    "max_drawdown": "maximize",
    "trade_count": "maximize",
}


@dataclass(frozen=True)
class OptimizerTrial:
    """Single parameter trial result — REQ-OPT-001."""

    trial_id: int
    parameters: dict[str, Any]
    aggregate_metrics: dict[str, Any]
    composite_score: float


@dataclass
class OptimizerResult:
    """Optimizer output bundle — REQ-OPT-001."""

    trials: list[OptimizerTrial] = field(default_factory=list)
    best_trial: OptimizerTrial | None = None
    method: str = "grid"


class StrategyOptimizer:
    """Grid/random/Bayesian search over walk-forward folds — REQ-OPT-001."""

    def __init__(
        self,
        validator: WalkForwardValidator,
        config: OptimizerConfig | None = None,
    ) -> None:
        self._validator = validator
        self._config = config or OptimizerConfig()

    def run(
        self,
        strategy: StrategyConfig,
        backtest: BacktestConfig,
        *,
        symbols: list[str] | None = None,
        dataset_version: str = "v1",
        start: date | None = None,
        end: date | None = None,
    ) -> OptimizerResult:
        """Evaluate parameter combinations and return ranked trials."""
        param_sets = self._generate_parameter_sets()
        trials: list[OptimizerTrial] = []

        for trial_id, overrides in enumerate(param_sets):
            trial_strategy = apply_strategy_overrides(strategy, overrides)
            summary = self._validator.run(
                trial_strategy,
                backtest,
                symbols=symbols,
                dataset_version=dataset_version,
                start=start,
                end=end,
            )
            composite = self._composite_score(summary.aggregate_metrics)
            trial = OptimizerTrial(
                trial_id=trial_id,
                parameters=overrides,
                aggregate_metrics=summary.aggregate_metrics,
                composite_score=composite,
            )
            trials.append(trial)
            log.info(
                "optimizer.trial_complete",
                trial_id=trial_id,
                composite=round(composite, 6),
                params=overrides,
            )

        trials.sort(key=lambda t: t.composite_score, reverse=True)
        best = trials[0] if trials else None
        return OptimizerResult(
            trials=trials,
            best_trial=best,
            method=self._config.method,
        )

    def _generate_parameter_sets(self) -> list[dict[str, Any]]:
        if self._config.method == "grid":
            return self._grid_sets()
        if self._config.method == "random":
            return self._random_sets()
        return self._bayesian_sets()

    def _grid_sets(self) -> list[dict[str, Any]]:
        value_lists = [self._values_for_spec(spec) for spec in self._config.parameters]
        if not value_lists:
            return [{}]
        combos = list(itertools.product(*value_lists))
        paths = [spec.path for spec in self._config.parameters]
        return [dict(zip(paths, combo, strict=True)) for combo in combos]

    def _random_sets(self) -> list[dict[str, Any]]:
        rng = random.Random(self._config.random_seed)
        sets: list[dict[str, Any]] = []
        for _ in range(self._config.max_trials):
            overrides: dict[str, Any] = {}
            for spec in self._config.parameters:
                values = self._values_for_spec(spec)
                overrides[spec.path] = rng.choice(values)
            sets.append(overrides)
        return sets

    def _bayesian_sets(self) -> list[dict[str, Any]]:
        """Sequential random-then-refined search (lightweight Bayesian proxy)."""
        rng = random.Random(self._config.random_seed)
        n_explore = max(3, min(self._config.max_trials // 3, 10))
        sets: list[dict[str, Any]] = []

        for _ in range(n_explore):
            overrides: dict[str, Any] = {}
            for spec in self._config.parameters:
                values = self._values_for_spec(spec)
                overrides[spec.path] = rng.choice(values)
            sets.append(overrides)

        while len(sets) < self._config.max_trials:
            base = rng.choice(sets[:n_explore])
            candidate = dict(base)
            spec = rng.choice(self._config.parameters)
            values = self._values_for_spec(spec)
            candidate[spec.path] = rng.choice(values)
            if candidate not in sets:
                sets.append(candidate)
        return sets[: self._config.max_trials]

    def _values_for_spec(self, spec: ParameterSpec) -> list[Any]:
        if spec.values:
            return list(spec.values)
        assert spec.min is not None and spec.max is not None
        if spec.type == "int":
            step = int(spec.step or 1)
            return list(range(int(spec.min), int(spec.max) + 1, step))
        step = spec.step or (spec.max - spec.min) / 10.0
        values: list[float] = []
        current = spec.min
        while current <= spec.max + 1e-9:
            values.append(round(current, 6))
            current += step
        return values or [spec.min]

    def _composite_score(self, metrics: dict[str, Any]) -> float:
        if metrics.get("fold_count", 0) == 0:
            return float("-inf")

        total_weight = 0.0
        score = 0.0
        for objective in self._config.objectives:
            weight = self._config.objective_weights.get(objective, 1.0)
            raw = metrics.get(f"{objective}_mean", metrics.get(objective))
            if raw is None:
                continue
            normalized = self._normalize_objective(objective, float(raw))
            score += weight * normalized
            total_weight += weight
        if total_weight <= 0:
            return float("-inf")
        return score / total_weight

    @staticmethod
    def _normalize_objective(objective: str, value: float) -> float:
        if objective == "max_drawdown":
            return max(min(-value, 1.0), 0.0)
        if objective in {"sharpe", "profit_factor", "win_rate"}:
            return max(min(value, 3.0) / 3.0, 0.0)
        if objective in {"total_return", "cagr"}:
            return max(min(value, 1.0), -1.0)
        return value

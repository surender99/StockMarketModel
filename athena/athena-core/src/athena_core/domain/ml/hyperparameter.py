"""Hyperparameter optimization — ATH-REL-011 §5.5, REQ-ML-OPTIMIZER-001."""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Any, Callable


@dataclass(frozen=True)
class HyperparameterResult:
    """Best hyperparameter trial."""

    params: dict[str, Any]
    score: float
    trial_index: int
    method: str


def grid_search(
    param_grid: dict[str, list[Any]],
    objective: Callable[[dict[str, Any]], float],
) -> HyperparameterResult:
    """Exhaustive grid search over parameter combinations."""
    keys = list(param_grid.keys())
    best_score = float("-inf")
    best_params: dict[str, Any] = {}
    best_idx = 0
    idx = 0

    def _recurse(depth: int, current: dict[str, Any]) -> None:
        nonlocal best_score, best_params, best_idx, idx
        if depth == len(keys):
            score = objective(current)
            if score > best_score:
                best_score = score
                best_params = dict(current)
                best_idx = idx
            idx += 1
            return
        key = keys[depth]
        for value in param_grid[key]:
            current[key] = value
            _recurse(depth + 1, current)

    _recurse(0, {})
    return HyperparameterResult(
        params=best_params,
        score=best_score,
        trial_index=best_idx,
        method="grid_search",
    )


def random_search(
    param_space: dict[str, tuple[Any, Any]],
    objective: Callable[[dict[str, Any]], float],
    *,
    n_trials: int = 10,
    seed: int = 42,
) -> HyperparameterResult:
    """Random search over numeric parameter ranges."""
    rng = random.Random(seed)
    best_score = float("-inf")
    best_params: dict[str, Any] = {}
    best_idx = 0
    for trial in range(n_trials):
        params: dict[str, Any] = {}
        for key, (lo, hi) in param_space.items():
            if isinstance(lo, int) and isinstance(hi, int):
                params[key] = rng.randint(lo, hi)
            else:
                params[key] = rng.uniform(float(lo), float(hi))
        score = objective(params)
        if score > best_score:
            best_score = score
            best_params = params
            best_idx = trial
    return HyperparameterResult(
        params=best_params,
        score=best_score,
        trial_index=best_idx,
        method="random_search",
    )


def bayesian_search(
    param_space: dict[str, tuple[float, float]],
    objective: Callable[[dict[str, Any]], float],
    *,
    n_trials: int = 5,
    seed: int = 42,
) -> HyperparameterResult:
    """Simplified Bayesian-style search (random + best refinement)."""
    initial = random_search(param_space, objective, n_trials=max(2, n_trials // 2), seed=seed)
    rng = random.Random(seed + 1)
    best = initial
    for trial in range(n_trials - initial.trial_index - 1):
        params: dict[str, Any] = {}
        for key, (lo, hi) in param_space.items():
            center = float(best.params.get(key, (lo + hi) / 2))
            span = (hi - lo) * 0.2
            params[key] = min(hi, max(lo, center + rng.uniform(-span, span)))
        score = objective(params)
        if score > best.score:
            best = HyperparameterResult(
                params=params,
                score=score,
                trial_index=trial + initial.trial_index + 1,
                method="bayesian_search",
            )
    return HyperparameterResult(
        params=best.params,
        score=best.score,
        trial_index=best.trial_index,
        method="bayesian_search",
    )

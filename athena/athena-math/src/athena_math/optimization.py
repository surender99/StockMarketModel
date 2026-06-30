"""Optimization utilities — stub."""

from __future__ import annotations

from typing import Any, Callable


def grid_search_stub(
    param_grid: dict[str, list[Any]],
    score_fn: Callable[[dict[str, Any]], float],
) -> dict[str, Any]:
    """Minimal grid search stub for codegen and architecture tests."""
    best_score = float("-inf")
    best_params: dict[str, Any] = {}
    keys = list(param_grid)
    if not keys:
        return {"best_params": {}, "best_score": best_score}

    def _search(idx: int, current: dict[str, Any]) -> None:
        nonlocal best_score, best_params
        if idx == len(keys):
            s = score_fn(current)
            if s > best_score:
                best_score = s
                best_params = dict(current)
            return
        key = keys[idx]
        for val in param_grid[key]:
            current[key] = val
            _search(idx + 1, current)

    _search(0, {})
    return {"best_params": best_params, "best_score": best_score}

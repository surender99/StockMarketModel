"""Regression analysis — ATH-REL-009 §5.8, REQ-STAT-REGRESSION-001."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class RegressionResult:
    """Linear regression fit summary — FR-006."""

    coefficients: dict[str, float]
    intercept: float
    r_squared: float
    adjusted_r_squared: float
    residual_std: float
    n_observations: int


def linear_regression(
    y: pd.Series | np.ndarray,
    x: pd.DataFrame | np.ndarray,
    *,
    feature_names: list[str] | None = None,
) -> RegressionResult:
    """Ordinary least squares linear regression — REQ-STAT-REGRESSION-001."""
    y_arr = np.asarray(y, dtype=float).reshape(-1)
    if isinstance(x, pd.DataFrame):
        names = list(x.columns)
        x_arr = x.astype(float).to_numpy()
    else:
        x_arr = np.asarray(x, dtype=float)
        if x_arr.ndim == 1:
            x_arr = x_arr.reshape(-1, 1)
        names = feature_names or [f"x{i}" for i in range(x_arr.shape[1])]

    mask = np.isfinite(y_arr)
    for col in range(x_arr.shape[1]):
        mask &= np.isfinite(x_arr[:, col])
    y_arr = y_arr[mask]
    x_arr = x_arr[mask]
    n, p = x_arr.shape[0], x_arr.shape[1]
    if n < p + 2:
        return RegressionResult({}, 0.0, 0.0, 0.0, 0.0, n)

    design = np.column_stack([np.ones(n), x_arr])
    beta, *_ = np.linalg.lstsq(design, y_arr, rcond=None)
    intercept = float(beta[0])
    coefs = {names[i]: float(beta[i + 1]) for i in range(p)}
    fitted = design @ beta
    residuals = y_arr - fitted
    ss_res = float(np.sum(residuals**2))
    ss_tot = float(np.sum((y_arr - y_arr.mean()) ** 2))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else 0.0
    adj_r2 = 1.0 - (1.0 - r2) * (n - 1) / (n - p - 1) if n > p + 1 else r2
    residual_std = float(np.sqrt(ss_res / (n - p - 1))) if n > p + 1 else 0.0

    return RegressionResult(
        coefficients=coefs,
        intercept=intercept,
        r_squared=float(r2),
        adjusted_r_squared=float(adj_r2),
        residual_std=residual_std,
        n_observations=n,
    )

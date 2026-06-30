"""Athena math — statistics facade over athena-core analytics."""

from athena_math.statistics import compute_correlation_matrix
from athena_math.regression import linear_regression_stub
from athena_math.probability import normal_cdf_stub
from athena_math.optimization import grid_search_stub

__all__ = [
    "compute_correlation_matrix",
    "grid_search_stub",
    "linear_regression_stub",
    "normal_cdf_stub",
]

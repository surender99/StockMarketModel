"""Statistical hypothesis tests — ATH-REL-009 §5.6, REQ-STAT-HYPOTHESIS-001."""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class HypothesisTestResult:
    """Result of a statistical hypothesis test — FR-003."""

    test_name: str
    statistic: float
    p_value: float
    significant: bool
    alpha: float
    sample_a: int
    sample_b: int | None = None


def student_t_test(
    sample_a: np.ndarray | list[float],
    sample_b: np.ndarray | list[float] | None = None,
    *,
    alpha: float = 0.05,
    equal_var: bool = True,
) -> HypothesisTestResult:
    """Two-sample or one-sample Student t-test — REQ-STAT-HYPOTHESIS-001."""
    a = np.asarray(sample_a, dtype=float)
    a = a[np.isfinite(a)]
    if sample_b is None:
        if a.size < 2:
            return HypothesisTestResult("student_t_one_sample", 0.0, 1.0, False, alpha, int(a.size))
        mean = a.mean()
        std = a.std(ddof=1)
        if std == 0:
            return HypothesisTestResult("student_t_one_sample", 0.0, 1.0, False, alpha, int(a.size))
        t_stat = float(mean / (std / math.sqrt(a.size)))
        df = a.size - 1
        p_val = float(2.0 * (1.0 - _t_cdf(abs(t_stat), df)))
        return HypothesisTestResult(
            "student_t_one_sample",
            t_stat,
            p_val,
            p_val < alpha,
            alpha,
            int(a.size),
        )

    b = np.asarray(sample_b, dtype=float)
    b = b[np.isfinite(b)]
    if a.size < 2 or b.size < 2:
        return HypothesisTestResult("student_t_two_sample", 0.0, 1.0, False, alpha, int(a.size), int(b.size))

    if equal_var:
        return _pooled_t_test(a, b, alpha=alpha)
    return _welch_t_test(a, b, alpha=alpha)


def welch_t_test(
    sample_a: np.ndarray | list[float],
    sample_b: np.ndarray | list[float],
    *,
    alpha: float = 0.05,
) -> HypothesisTestResult:
    """Welch's unequal variance t-test."""
    return student_t_test(sample_a, sample_b, alpha=alpha, equal_var=False)


def mann_whitney_u_test(
    sample_a: np.ndarray | list[float],
    sample_b: np.ndarray | list[float],
    *,
    alpha: float = 0.05,
) -> HypothesisTestResult:
    """Mann-Whitney U test (normal approximation for p-value)."""
    a = np.sort(np.asarray(sample_a, dtype=float))
    b = np.sort(np.asarray(sample_b, dtype=float))
    a = a[np.isfinite(a)]
    b = b[np.isfinite(b)]
    n1, n2 = a.size, b.size
    if n1 == 0 or n2 == 0:
        return HypothesisTestResult("mann_whitney_u", 0.0, 1.0, False, alpha, n1, n2)

    combined = np.concatenate([a, b])
    ranks = _rankdata(combined)
    r1 = float(ranks[:n1].sum())
    u1 = r1 - n1 * (n1 + 1) / 2.0
    u = min(u1, n1 * n2 - u1)
    mu = n1 * n2 / 2.0
    sigma = math.sqrt(n1 * n2 * (n1 + n2 + 1) / 12.0)
    if sigma == 0:
        return HypothesisTestResult("mann_whitney_u", float(u), 1.0, False, alpha, n1, n2)
    z = (u - mu) / sigma
    p_val = float(2.0 * (1.0 - _normal_cdf(abs(z))))
    return HypothesisTestResult("mann_whitney_u", float(u), p_val, p_val < alpha, alpha, n1, n2)


def _pooled_t_test(a: np.ndarray, b: np.ndarray, *, alpha: float) -> HypothesisTestResult:
    n1, n2 = a.size, b.size
    v1, v2 = a.var(ddof=1), b.var(ddof=1)
    pooled = ((n1 - 1) * v1 + (n2 - 1) * v2) / (n1 + n2 - 2)
    if pooled <= 0:
        return HypothesisTestResult("student_t_two_sample", 0.0, 1.0, False, alpha, n1, n2)
    se = math.sqrt(pooled * (1.0 / n1 + 1.0 / n2))
    t_stat = float((a.mean() - b.mean()) / se)
    df = n1 + n2 - 2
    p_val = float(2.0 * (1.0 - _t_cdf(abs(t_stat), df)))
    return HypothesisTestResult("student_t_two_sample", t_stat, p_val, p_val < alpha, alpha, n1, n2)


def _welch_t_test(a: np.ndarray, b: np.ndarray, *, alpha: float) -> HypothesisTestResult:
    n1, n2 = a.size, b.size
    v1, v2 = a.var(ddof=1), b.var(ddof=1)
    se = math.sqrt(v1 / n1 + v2 / n2)
    if se == 0:
        return HypothesisTestResult("welch_t", 0.0, 1.0, False, alpha, n1, n2)
    t_stat = float((a.mean() - b.mean()) / se)
    num = (v1 / n1 + v2 / n2) ** 2
    den = (v1 / n1) ** 2 / (n1 - 1) + (v2 / n2) ** 2 / (n2 - 1)
    df = num / den if den > 0 else n1 + n2 - 2
    p_val = float(2.0 * (1.0 - _t_cdf(abs(t_stat), df)))
    return HypothesisTestResult("welch_t", t_stat, p_val, p_val < alpha, alpha, n1, n2)


def _rankdata(arr: np.ndarray) -> np.ndarray:
    order = np.argsort(arr)
    ranks = np.empty_like(order, dtype=float)
    ranks[order] = np.arange(1, len(arr) + 1, dtype=float)
    return ranks


def _normal_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def _t_cdf(t: float, df: float) -> float:
    """Approximate two-sided t CDF via regularized incomplete beta."""
    if df <= 0:
        return 0.5
    x = df / (df + t * t)
    ib = _regularized_incomplete_beta(df / 2.0, 0.5, x)
    return 1.0 - 0.5 * ib


def _regularized_incomplete_beta(a: float, b: float, x: float) -> float:
    """Continued fraction approximation for I_x(a,b)."""
    if x <= 0:
        return 0.0
    if x >= 1:
        return 1.0
    ln_beta = math.lgamma(a) + math.lgamma(b) - math.lgamma(a + b)
    front = math.exp(a * math.log(x) + b * math.log(1.0 - x) - ln_beta) / a
    cf = _betacf(a, b, x)
    return front * cf


def _betacf(a: float, b: float, x: float) -> float:
    max_iter = 200
    eps = 3e-7
    am = 1.0
    bm = 1.0
    az = 1.0
    qab = a + b
    qap = a + 1.0
    qam = a - 1.0
    bz = 1.0 - qab * x / qap
    for m in range(1, max_iter + 1):
        em = float(m)
        tem = em + em
        d = em * (b - em) * x / ((qam + tem) * (a + tem))
        ap = az + d * am
        bp = bz + d * bm
        d = -(a + em) * (qab + em) * x / ((a + tem) * (qap + tem))
        app = ap + d * az
        bpp = bp + d * bz
        am = ap / bpp
        bm = bp / bpp
        az = app / bpp
        bz = 1.0
        if abs(az - app / bpp) < eps * abs(az):
            return az
    return az

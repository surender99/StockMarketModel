"""Quantitative Analytics APS catalog — PHASE 8 QARIP."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

AnalyticsStatus = Literal["MVP", "Partial", "Deferred"]


@dataclass(frozen=True, slots=True)
class AnalyticsCatalogEntry:
    aps_id: str
    name: str
    domain: str
    status: AnalyticsStatus


def _a(
    aps_id: str,
    name: str,
    domain: str,
    status: AnalyticsStatus = "Deferred",
) -> AnalyticsCatalogEntry:
    return AnalyticsCatalogEntry(aps_id, name, domain, status)


ANALYTICS_CATALOG: tuple[AnalyticsCatalogEntry, ...] = (
    # Statistics-Engine
    _a("APS-STAT-CORE-001", "Statistics Core Framework", "Statistics-Engine", "MVP"),
    _a("APS-STAT-DESCRIPTIVE-001", "Descriptive Statistics", "Statistics-Engine", "MVP"),
    _a("APS-STAT-DISTRIBUTION-001", "Distribution Support", "Statistics-Engine", "Partial"),
    _a("APS-STAT-MOMENTS-001", "Statistical Moments", "Statistics-Engine", "MVP"),
    _a("APS-STAT-MEAN-001", "Mean Calculation", "Statistics-Engine", "MVP"),
    _a("APS-STAT-MEDIAN-001", "Median Calculation", "Statistics-Engine", "MVP"),
    _a("APS-STAT-MODE-001", "Mode Calculation", "Statistics-Engine"),
    _a("APS-STAT-VARIANCE-001", "Variance Calculation", "Statistics-Engine", "MVP"),
    _a("APS-STAT-STDDEV-001", "Standard Deviation", "Statistics-Engine", "MVP"),
    _a("APS-STAT-MAD-001", "Median Absolute Deviation", "Statistics-Engine", "Partial"),
    _a("APS-STAT-RANGE-001", "Range Calculation", "Statistics-Engine", "MVP"),
    _a("APS-STAT-QUANTILE-001", "Quantile Calculation", "Statistics-Engine", "Partial"),
    _a("APS-STAT-PERCENTILE-001", "Percentile Calculation", "Statistics-Engine", "Partial"),
    _a("APS-STAT-ZSCORE-001", "Z-Score Normalization", "Statistics-Engine"),
    _a("APS-STAT-OUTLIER-001", "Outlier Detection", "Statistics-Engine"),
    # Probability-Engine
    _a("APS-PROB-CORE-001", "Probability Framework", "Probability-Engine", "Partial"),
    _a("APS-PROB-BAYES-001", "Bayesian Probability", "Probability-Engine"),
    _a("APS-PROB-CONDITIONAL-001", "Conditional Probability", "Probability-Engine"),
    _a("APS-PROB-JOINT-001", "Joint Probability", "Probability-Engine"),
    _a("APS-PROB-LIKELIHOOD-001", "Likelihood Estimation", "Probability-Engine"),
    _a("APS-PROB-EXPECTEDVALUE-001", "Expected Value", "Probability-Engine"),
    _a("APS-PROB-PRIOR-001", "Prior Distribution", "Probability-Engine"),
    _a("APS-PROB-POSTERIOR-001", "Posterior Update", "Probability-Engine"),
    _a("APS-PROB-ENTROPY-001", "Entropy", "Probability-Engine"),
    _a("APS-PROB-MARGINAL-001", "Marginal Probability", "Probability-Engine"),
    # Hypothesis-Testing
    _a("APS-HYP-TTEST-001", "Student t Test", "Hypothesis-Testing"),
    _a("APS-HYP-WELCH-001", "Welch Test", "Hypothesis-Testing"),
    _a("APS-HYP-MANNWHITNEY-001", "Mann Whitney U", "Hypothesis-Testing"),
    _a("APS-HYP-WILCOXON-001", "Wilcoxon Signed Rank", "Hypothesis-Testing"),
    _a("APS-HYP-KS-001", "Kolmogorov Smirnov", "Hypothesis-Testing"),
    _a("APS-HYP-SHAPIRO-001", "Normality Tests", "Hypothesis-Testing"),
    _a("APS-HYP-ANOVA-001", "ANOVA", "Hypothesis-Testing"),
    _a("APS-HYP-CHISQ-001", "Chi Square Test", "Hypothesis-Testing"),
    _a("APS-HYP-SIGN-001", "Sign Test", "Hypothesis-Testing"),
    _a("APS-HYP-RUNS-001", "Runs Test", "Hypothesis-Testing"),
    _a("APS-HYP-POWER-001", "Statistical Power", "Hypothesis-Testing"),
    _a("APS-HYP-MULTIPLE-001", "Multiple Comparison Correction", "Hypothesis-Testing"),
    # Analytics-Correlation
    _a("APS-CORR-PEARSON-001", "Pearson Correlation", "Analytics-Correlation", "Partial"),
    _a("APS-CORR-SPEARMAN-001", "Spearman Correlation", "Analytics-Correlation"),
    _a("APS-CORR-KENDALL-001", "Kendall Tau", "Analytics-Correlation"),
    _a("APS-CORR-PARTIAL-001", "Partial Correlation", "Analytics-Correlation"),
    _a("APS-CORR-CROSS-001", "Cross Correlation", "Analytics-Correlation"),
    _a("APS-CORR-MUTUALINFO-001", "Mutual Information", "Analytics-Correlation"),
    _a("APS-CORR-MATRIX-001", "Correlation Matrix", "Analytics-Correlation", "Partial"),
    _a("APS-CORR-ROLLING-001", "Rolling Correlation", "Analytics-Correlation"),
    _a("APS-CORR-DIVERSIFICATION-001", "Diversification Score", "Analytics-Correlation"),
    _a("APS-CORR-STABILITY-001", "Correlation Stability", "Analytics-Correlation"),
    # Regression-Platform
    _a("APS-REG-LINEAR-001", "Linear Regression", "Regression-Platform"),
    _a("APS-REG-POLY-001", "Polynomial Regression", "Regression-Platform"),
    _a("APS-REG-RIDGE-001", "Ridge Regression", "Regression-Platform"),
    _a("APS-REG-LASSO-001", "LASSO Regression", "Regression-Platform"),
    _a("APS-REG-ROBUST-001", "Robust Regression", "Regression-Platform"),
    _a("APS-REG-DIAGNOSTICS-001", "Residual Analysis", "Regression-Platform"),
    _a("APS-REG-LOGISTIC-001", "Logistic Regression", "Regression-Platform"),
    _a("APS-REG-ELASTICNET-001", "Elastic Net Regression", "Regression-Platform"),
    _a("APS-REG-MULTIVARIATE-001", "Multivariate Regression", "Regression-Platform"),
    _a("APS-REG-FORECAST-001", "Regression Forecast", "Regression-Platform"),
    # Risk-Intelligence
    _a("APS-RISK-VAR-001", "Value at Risk", "Risk-Intelligence", "Partial"),
    _a("APS-RISK-CVAR-001", "Conditional VaR", "Risk-Intelligence", "Partial"),
    _a("APS-RISK-DRAWDOWN-001", "Drawdown Analysis", "Risk-Intelligence", "MVP"),
    _a("APS-RISK-DOWNSIDE-001", "Downside Risk", "Risk-Intelligence", "Partial"),
    _a("APS-RISK-TAIL-001", "Tail Risk", "Risk-Intelligence", "Partial"),
    _a("APS-RISK-ULCER-001", "Ulcer Index", "Risk-Intelligence"),
    _a("APS-RISK-RECOVERY-001", "Recovery Metrics", "Risk-Intelligence"),
    _a("APS-RISK-VOLATILITY-001", "Volatility", "Risk-Intelligence", "MVP"),
    _a("APS-RISK-SORTINO-001", "Sortino Risk", "Risk-Intelligence", "Partial"),
    _a("APS-RISK-SEMVOL-001", "Semi Volatility", "Risk-Intelligence", "Partial"),
    _a("APS-RISK-BETA-001", "Beta Risk", "Risk-Intelligence", "Partial"),
    _a("APS-RISK-STRESS-001", "Stress VaR", "Risk-Intelligence"),
    _a("APS-RISK-CONCENTRATION-001", "Concentration Risk", "Risk-Intelligence"),
    _a("APS-RISK-LEVERAGE-001", "Leverage Risk", "Risk-Intelligence"),
    _a("APS-RISK-EXPECTATION-001", "Tail Expectation", "Risk-Intelligence"),
    # Performance-Analytics
    _a("APS-PERF-CAGR-001", "CAGR", "Performance-Analytics", "MVP"),
    _a("APS-PERF-SHARPE-001", "Sharpe Ratio", "Performance-Analytics", "MVP"),
    _a("APS-PERF-SORTINO-001", "Sortino Ratio", "Performance-Analytics", "MVP"),
    _a("APS-PERF-CALMAR-001", "Calmar Ratio", "Performance-Analytics", "Partial"),
    _a("APS-PERF-OMEGA-001", "Omega Ratio", "Performance-Analytics"),
    _a("APS-PERF-PROFITFACTOR-001", "Profit Factor", "Performance-Analytics", "MVP"),
    _a("APS-PERF-EXPECTANCY-001", "Expectancy", "Performance-Analytics", "Partial"),
    _a("APS-PERF-ATTRIBUTION-001", "Performance Attribution", "Performance-Analytics"),
    _a("APS-PERF-TOTALRETURN-001", "Total Return", "Performance-Analytics", "MVP"),
    _a("APS-PERF-WINRATE-001", "Win Rate", "Performance-Analytics", "MVP"),
    _a("APS-PERF-AVGWIN-001", "Average Win", "Performance-Analytics", "Partial"),
    _a("APS-PERF-AVGLOSS-001", "Average Loss", "Performance-Analytics", "Partial"),
    _a("APS-PERF-INFORMATION-001", "Information Ratio", "Performance-Analytics"),
    _a("APS-PERF-TREYNOR-001", "Treynor Ratio", "Performance-Analytics"),
    _a("APS-PERF-MAXCONSEC-001", "Max Consecutive Wins", "Performance-Analytics"),
    # Analytics-Monte-Carlo
    _a("APS-MC-CORE-001", "Monte Carlo Core", "Analytics-Monte-Carlo", "Partial"),
    _a("APS-MC-BOOTSTRAP-001", "Bootstrap", "Analytics-Monte-Carlo", "Partial"),
    _a("APS-MC-PERMUTATION-001", "Permutation Testing", "Analytics-Monte-Carlo"),
    _a("APS-MC-RISK-001", "Risk Simulation", "Analytics-Monte-Carlo"),
    _a("APS-MC-PROBABILITYRUIN-001", "Probability of Ruin", "Analytics-Monte-Carlo"),
    _a("APS-MC-TRADE-001", "Trade Randomization", "Analytics-Monte-Carlo"),
    _a("APS-MC-RETURN-001", "Return Sampling", "Analytics-Monte-Carlo"),
    _a("APS-MC-PATH-001", "Path Simulation", "Analytics-Monte-Carlo"),
    _a("APS-MC-CONFIDENCE-001", "Confidence Intervals", "Analytics-Monte-Carlo", "Partial"),
    _a("APS-MC-STRESS-001", "Monte Carlo Stress", "Analytics-Monte-Carlo"),
    # Optimization-Analytics
    _a("APS-OPT-SENSITIVITY-001", "Sensitivity Analysis", "Optimization-Analytics"),
    _a("APS-OPT-PARAMETER-001", "Parameter Stability", "Optimization-Analytics"),
    _a("APS-OPT-HEATMAP-001", "Parameter Heat Maps", "Optimization-Analytics"),
    _a("APS-OPT-ROBUSTNESS-001", "Robust Region Detection", "Optimization-Analytics"),
    _a("APS-OPT-GRID-001", "Grid Search Analytics", "Optimization-Analytics"),
    _a("APS-OPT-WALKFORWARD-001", "Walk Forward Optimization", "Optimization-Analytics"),
    _a("APS-OPT-STABILITY-001", "Stability Score", "Optimization-Analytics"),
    _a("APS-OPT-CURVEFIT-001", "Curve Fitting Detection", "Optimization-Analytics"),
    _a("APS-OPT-OOS-001", "Out of Sample Validation", "Optimization-Analytics"),
    _a("APS-OPT-OVERFIT-001", "Overfitting Detection", "Optimization-Analytics"),
    # Time-Series-Analytics
    _a("APS-TS-STATIONARITY-001", "Stationarity Tests", "Time-Series-Analytics"),
    _a("APS-TS-AUTOCORR-001", "Autocorrelation", "Time-Series-Analytics"),
    _a("APS-TS-PACF-001", "Partial Autocorrelation", "Time-Series-Analytics"),
    _a("APS-TS-SEASONALITY-001", "Seasonality Detection", "Time-Series-Analytics"),
    _a("APS-TS-DECOMPOSITION-001", "Time Series Decomposition", "Time-Series-Analytics"),
    _a("APS-TS-ADF-001", "ADF Test", "Time-Series-Analytics"),
    _a("APS-TS-KPSS-001", "KPSS Test", "Time-Series-Analytics"),
    _a("APS-TS-SMOOTHING-001", "Smoothing", "Time-Series-Analytics"),
    _a("APS-TS-DIFF-001", "Differencing", "Time-Series-Analytics"),
    _a("APS-TS-LAG-001", "Lag Features", "Time-Series-Analytics"),
    _a("APS-TS-ROLLING-001", "Rolling Statistics", "Time-Series-Analytics"),
    _a("APS-TS-FORECAST-001", "Time Series Forecast", "Time-Series-Analytics"),
    # Factor-Analytics
    _a("APS-FACTOR-BETA-001", "Beta", "Factor-Analytics", "Partial"),
    _a("APS-FACTOR-ALPHA-001", "Alpha", "Factor-Analytics", "Partial"),
    _a("APS-FACTOR-MULTI-001", "Multi Factor Models", "Factor-Analytics"),
    _a("APS-FACTOR-FAMA-001", "Fama French", "Factor-Analytics"),
    _a("APS-FACTOR-MOMENTUM-001", "Momentum Factor", "Factor-Analytics"),
    _a("APS-FACTOR-SIZE-001", "Size Factor", "Factor-Analytics"),
    _a("APS-FACTOR-VALUE-001", "Value Factor", "Factor-Analytics"),
    _a("APS-FACTOR-EXPOSURE-001", "Factor Exposure", "Factor-Analytics"),
    # Scenario-Analysis
    _a("APS-SCENARIO-STRESS-001", "Stress Testing", "Scenario-Analysis"),
    _a("APS-SCENARIO-SHOCK-001", "Market Shock", "Scenario-Analysis"),
    _a("APS-SCENARIO-CRASH-001", "Crash Scenarios", "Scenario-Analysis"),
    _a("APS-SCENARIO-INFLATION-001", "Macro Scenarios", "Scenario-Analysis"),
    _a("APS-SCENARIO-RATE-001", "Rate Shock", "Scenario-Analysis"),
    _a("APS-SCENARIO-LIQUIDITY-001", "Liquidity Crisis", "Scenario-Analysis"),
    _a("APS-SCENARIO-BLACKSWAN-001", "Black Swan", "Scenario-Analysis"),
    _a("APS-SCENARIO-HISTORICAL-001", "Historical Replay", "Scenario-Analysis"),
    # Analytics-Validation
    _a("APS-VALIDATE-STATS-001", "Numerical Validation", "Analytics-Validation", "Partial"),
    _a("APS-VALIDATE-RISK-001", "Risk Metric Validation", "Analytics-Validation", "Partial"),
    _a("APS-VALIDATE-MODELS-001", "Reference Comparisons", "Analytics-Validation"),
    _a("APS-VALIDATE-GOLDEN-001", "Golden Dataset Validation", "Analytics-Validation", "Partial"),
    _a("APS-VALIDATE-CROSSLIB-001", "Cross Library Validation", "Analytics-Validation"),
    _a("APS-VALIDATE-PRECISION-001", "Numerical Precision", "Analytics-Validation"),
    _a("APS-VALIDATE-DETERMINISM-001", "Deterministic Replay", "Analytics-Validation"),
    _a("APS-VALIDATE-TOLERANCE-001", "Floating Point Tolerance", "Analytics-Validation"),
    _a("APS-VALIDATE-REGRESSION-001", "Regression Test Suite", "Analytics-Validation"),
    _a("APS-VALIDATE-CONSISTENCY-001", "Cross Module Consistency", "Analytics-Validation", "Partial"),
    # Quantitative-Reporting
    _a("APS-REPORT-QUANT-001", "Quantitative Reports", "Quantitative-Reporting", "Partial"),
    _a("APS-REPORT-RISK-001", "Risk Reports", "Quantitative-Reporting", "Partial"),
    _a("APS-REPORT-PERFORMANCE-001", "Performance Reports", "Quantitative-Reporting", "Partial"),
    _a("APS-REPORT-COMPARISON-001", "Strategy Comparison", "Quantitative-Reporting"),
    _a("APS-REPORT-SUMMARY-001", "Analytics Summary", "Quantitative-Reporting", "Partial"),
    _a("APS-REPORT-DETAIL-001", "Detailed Analytics Report", "Quantitative-Reporting"),
    _a("APS-REPORT-EXPORT-001", "Report Export", "Quantitative-Reporting"),
    _a("APS-REPORT-SCHEDULE-001", "Scheduled Reports", "Quantitative-Reporting"),
    # Analytics-Benchmarking
    _a("APS-BENCH-SPEED-001", "Analytics Speed Benchmark", "Analytics-Benchmarking"),
    _a("APS-BENCH-MEMORY-001", "Memory Benchmark", "Analytics-Benchmarking"),
    _a("APS-BENCH-PRECISION-001", "Numerical Precision Benchmark", "Analytics-Benchmarking"),
    _a("APS-BENCH-CROSSLIB-001", "Cross Library Benchmark", "Analytics-Benchmarking"),
    _a("APS-BENCH-DETERMINISM-001", "Determinism Benchmark", "Analytics-Benchmarking"),
    _a("APS-BENCH-REPLAY-001", "Replay Benchmark", "Analytics-Benchmarking"),
    _a("APS-BENCH-TOLERANCE-001", "Tolerance Verification", "Analytics-Benchmarking"),
)


def list_mvp_analytics() -> list[AnalyticsCatalogEntry]:
    return [e for e in ANALYTICS_CATALOG if e.status == "MVP"]


def lookup_analytics_aps(aps_id: str) -> AnalyticsCatalogEntry | None:
    for entry in ANALYTICS_CATALOG:
        if entry.aps_id == aps_id:
            return entry
    return None

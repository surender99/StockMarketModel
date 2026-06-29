# ATH-REL-009 Statistics & Analytics Engine — Section Index



> **Release package:** [ATH-REL-009-Statistics-and-Analytics-Engine.md](../ATH-REL-009-Statistics-and-Analytics-Engine.md)  

> **Source doc:** `References/REL-009-Statistics and Analytics Engine.docx`



This index maps the ATH-REL-009 Release-09 module taxonomy to canonical specs and `athena-core` modules.



---



## Section Map



| Section | Doc Status (v0.1) | Canonical Spec | Code / Tooling |

|---------|-------------------|----------------|----------------|

| **00 Executive Summary** | From docx §1 | [ATH-REL-009](../ATH-REL-009-Statistics-and-Analytics-Engine.md) | — |

| **01 Statistics Framework** | From docx §5.1 | [AES-1100](../statistics/framework/AES-1100-Statistics.md) | `application/statistics_manager.py` |

| **02 Performance Metrics** | From docx §5.2 | [REQ-STAT-001](../statistics/requirements/REQ-STAT-001.md) | `application/statistics_engine.py` |

| **03 Risk Metrics** | From docx §5.3 | [REQ-STAT-RISK-001](../requirements/REQ-STAT-RISK-001.md) | `domain/statistics/risk_metrics.py` |

| **04 Risk Adjusted Returns** | From docx §5.4 | — | `backtest_metrics.py`, `portfolio_analytics.py` |

| **05 Distribution Analysis** | From docx §5.5 | [REQ-STAT-DIST-001](../requirements/REQ-STAT-DIST-001.md) | `domain/statistics/distribution.py` |

| **06 Statistical Tests** | From docx §5.6 | [REQ-STAT-HYPOTHESIS-001](../requirements/REQ-STAT-HYPOTHESIS-001.md) | `domain/statistics/hypothesis.py` |

| **07 Correlation Analysis** | From docx §5.7 | [REQ-STAT-CORR-001](../requirements/REQ-STAT-CORR-001.md) | `domain/statistics/correlation.py` |

| **08 Regression Analysis** | From docx §5.8 | [REQ-STAT-REGRESSION-001](../requirements/REQ-STAT-REGRESSION-001.md) | `domain/statistics/regression.py` |

| **09 Probability Analysis** | From docx §5.9 | [REQ-STAT-003](../statistics/requirements/REQ-STAT-003.md) | `statistics_engine.py` |

| **10 Confidence Analysis** | From docx §5.10 | [REQ-STAT-002](../statistics/requirements/REQ-STAT-002.md) | `analytics_engine.py` |

| **11 Robustness Testing** | From docx §5.11 | [REQ-WALK-FORWARD-001](../requirements/REQ-WALK-FORWARD-001.md) | `analytics_engine.py` |

| **12 Optimization Analysis** | From docx §5.12 | [REQ-OPT-001](../requirements/REQ-OPT-001.md) | `analytics_engine.py` |

| **13 Reporting Engine** | From docx §5.13 | [REQ-STAT-REPORT-001](../requirements/REQ-STAT-REPORT-001.md) | `application/analytics_reporting.py` |

| **14 Testing** | From docx §9 | [ATH-002](../ATH-002-Engineering-Standards.md) | `tests/test_statistics_engine_framework.py` |

| **15 Benchmarks** | From docx §10 | [athena-core/benchmarks/](../../athena-core/benchmarks/README.md) | `tests/benchmarks/` |

| **16 AI Coding** | From docx §11 | [AES-0006](../governance/AES-0006-AI-Coding-Standards.md) | — |

| **17 Agent Packages** | From docx §8 | [prompts/](../prompts/) | — |

| **18 Playbooks** | — | [athena-docs/handbook/](../../athena-docs/handbook/) | — |



---



## REQ Traceability (Release-09)



| REQ ID | Section | Module |

|--------|---------|--------|

| REQ-STAT-001 | 02 Performance Metrics | `application/statistics_engine.py` |

| REQ-STAT-002 | 10 Confidence Analysis | `statistics_engine.py` |

| REQ-STAT-003 | 09 Probability Analysis | `statistics_engine.py` |

| REQ-STAT-DIST-001 | 05 Distribution Analysis | `domain/statistics/distribution.py` |

| REQ-STAT-HYPOTHESIS-001 | 06 Statistical Tests | `domain/statistics/hypothesis.py` |

| REQ-STAT-RISK-001 | 03 Risk Metrics | `domain/statistics/risk_metrics.py` |

| REQ-STAT-CORR-001 | 07 Correlation Analysis | `domain/statistics/correlation.py` |

| REQ-STAT-REGRESSION-001 | 08 Regression Analysis | `domain/statistics/regression.py` |

| REQ-STAT-REPORT-001 | 13 Reporting Engine | `application/analytics_reporting.py` |

| FR-012 | 01 Statistics Framework | `application/statistics_manager.py` |

| FR-014 | 01 Statistics Framework | `application/analytics_engine.py` |

| FR-015 | 01 Statistics Framework | `domain/statistics/statistics_plugins.py` |


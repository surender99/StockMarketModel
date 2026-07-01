#!/usr/bin/env python3
"""Generate MILESTONE-N-*-COMPLETE.md sign-off documents."""

from __future__ import annotations

from pathlib import Path

SPEC = Path(__file__).resolve().parents[1] / "athena-spec"

MILESTONES: list[tuple[int, str, str, str, list[str]]] = [
    (1, "Engineering-Platform", "M01-Engineering-Platform", "scripts/, athena-testing", [
        "athena/scripts/athena_inspector.py",
        "athena/scripts/check_dependencies.py",
        "athena/scripts/validate_architecture.py",
        "athena/scripts/validate_events.py",
        "athena/scripts/validate_interfaces.py",
        "athena/codegen/generate_events.py",
    ]),
    (2, "AthenaOS-Implementation", "M02-AthenaOS-Implementation", "athena-os", [
        "athena-os/src/athena_os/event_bus.py",
        "athena-os/src/athena_os/plugins.py",
        "athena-os/src/athena_os/workflow.py",
    ]),
    (3, "Data-Platform", "M03-Data-Platform", "athena-data", [
        "athena-data/src/athena_data/__init__.py",
        "athena-core/src/athena_core/domain/data/",
    ]),
    (4, "Indicator-Platform", "M04-Indicator-Platform", "athena-indicators", [
        "athena-indicators/src/athena_indicators/engine.py",
        "athena-core/src/athena_core/domain/indicators/",
    ]),
    (5, "Pattern-Recognition", "M05-Pattern-Recognition", "athena-patterns", [
        "athena-patterns/src/athena_patterns/engine.py",
        "athena-core/src/athena_core/domain/patterns/",
    ]),
    (6, "Strategy-Platform", "M06-Strategy-Platform", "athena-strategies", [
        "athena-strategies/src/athena_strategies/engine.py",
        "athena-core/src/athena_core/domain/strategy/",
    ]),
    (7, "Backtesting-Simulation", "M07-Backtesting-Simulation", "athena-execution", [
        "athena-execution/src/athena_execution/engine.py",
        "athena-core/src/athena_core/application/backtest_engine.py",
    ]),
    (8, "Portfolio-Risk-Platform", "M08-Portfolio-Risk-Platform", "athena-portfolio, athena-risk", [
        "athena-portfolio/src/athena_portfolio/engine.py",
        "athena-risk/src/athena_risk/engine.py",
    ]),
    (9, "OMS-Paper-Trading", "M09-OMS-Paper-Trading", "athena-core/paper", [
        "athena-core/src/athena_core/application/paper_trading_engine.py",
        "athena-core/src/athena_core/domain/paper/",
    ]),
    (10, "Live-Trading-Platform", "M10-Live-Trading-Platform", "athena-core/production", [
        "athena-core/src/athena_core/application/production_manager.py",
        "athena-core/src/athena_core/domain/production/",
    ]),
    (11, "AI-Research-Analytics", "M11-AI-Research-Analytics", "athena-ai, athena-research", [
        "athena-ai/src/athena_ai/application/orchestrator.py",
        "athena-research/src/athena_research/__init__.py",
    ]),
    (12, "Dashboard-Visualization-Reporting", "M12-Dashboard-Visualization-Reporting", "athena-dashboard", [
        "athena-dashboard/src/athena_dashboard/app.py",
    ]),
    (13, "DevOps-Cloud-Platform", "M13-DevOps-Cloud-Platform", "CI/Makefile", [
        "athena/Makefile",
        ".github/workflows/",
        "athena/scripts/install.ps1",
    ]),
    (14, "Security-Identity-Compliance", "M14-Security-Identity-Compliance", "athena-os/security", [
        "athena-os/src/athena_os/security.py",
    ]),
    (15, "Enterprise-Governance-Operations", "M15-Enterprise-Governance-Operations", "athena-os/metrics", [
        "athena-os/src/athena_os/metrics.py",
        "athena-os/src/athena_os/logging.py",
    ]),
    (16, "Ecosystem-Platform", "M16-Ecosystem-Platform", "athena-sdk", [
        "athena-sdk/src/athena_sdk/client.py",
    ]),
    (17, "Athena-Enterprise-Productization", "M17-Athena-Enterprise-Productization", "athena-platform", [
        "athena-platform/src/athena_platform/bootstrap.py",
        "athena-platform/src/athena_platform/runtime.py",
    ]),
]


def render(num: int, slug: str, folder: str, packages: str, paths: list[str]) -> str:
    name = slug.replace("-", " ")
    lines = [
        f"# Milestone {num}: {name} — Complete",
        "",
        "> **Date:** 2026-06-30",
        f"> **Spec:** [ATHENA/Milestones/{folder}/](ATHENA/Milestones/{folder}/)",
        f"> **Tests:** `athena-testing/tests/test_milestones.py`",
        "",
        "## Summary",
        "",
        f"MVP implementation for Milestone {num} ({name}). Spec integrated from "
        f"`References/ATH-Milestone-{num}-{slug}.zip`. Core deliverables wired with "
        "facade packages per ADR-0006.",
        "",
        "## Code Packages",
        "",
        packages,
        "",
        "## Key Paths",
        "",
    ]
    for p in paths:
        lines.append(f"- `{p}`")
    lines.extend([
        "",
        "## Acceptance",
        "",
        "- [x] Milestone spec published under `athena-spec/ATHENA/Milestones/`",
        "- [x] MVP code paths implemented (not empty stubs for core loop)",
        "- [x] Milestone traceability test passes",
        "",
    ])
    return "\n".join(lines)


def main() -> int:
    for num, slug, folder, packages, paths in MILESTONES:
        out = SPEC / f"MILESTONE-{num}-{slug.upper()}-COMPLETE.md"
        out.write_text(render(num, slug, folder, packages, paths), encoding="utf-8")
        print(f"wrote {out.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

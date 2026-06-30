"""Integrate References/ ATH-Milestone-*.zip archives into athena-spec."""
from __future__ import annotations

import re
import shutil
import zipfile
from dataclasses import dataclass
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
REFERENCES = REPO / "References"
SPEC = REPO / "athena" / "athena-spec"
MILESTONES_ROOT = SPEC / "ATHENA" / "Milestones"


@dataclass(frozen=True)
class MilestoneConfig:
    number: int
    slug: str
    title: str
    zip_name: str
    package_kind: str  # "engineering-spec" | "implementation-package"
    rel_phase: str | None = None
    code_modules: tuple[str, ...] = ()


MILESTONES: list[MilestoneConfig] = [
    MilestoneConfig(
        1,
        "Engineering-Platform",
        "Engineering Platform",
        "ATH-Milestone-1-Engineering-Platform.zip",
        "engineering-spec",
        "REL-000",
        (
            "athena/scripts/check_dependencies.py",
            "athena/scripts/athena_inspector.py",
            "athena/scripts/generate_dependency_graph.py",
            "athena/scripts/generate_events.py",
            "athena/scripts/generate_docs.py",
        ),
    ),
    MilestoneConfig(
        2,
        "AthenaOS-Implementation",
        "AthenaOS Implementation",
        "ATH-Milestone-2-AthenaOS-Implementation.zip",
        "implementation-package",
        "ATH-001",
        ("athena/athena-os/",),
    ),
    MilestoneConfig(
        3,
        "Data-Platform",
        "Data Platform",
        "ATH-Milestone-3-Data-Platform.zip",
        "implementation-package",
        "REL-002",
        ("athena/athena-data/", "athena/athena-core/src/athena_core/domain/data/"),
    ),
    MilestoneConfig(
        4,
        "Indicator-Platform",
        "Indicator Platform",
        "ATH-Milestone-4-Indicator-Platform.zip",
        "implementation-package",
        "REL-004",
        ("athena/athena-indicators/",),
    ),
    MilestoneConfig(
        5,
        "Pattern-Recognition",
        "Pattern Recognition",
        "ATH-Milestone-5-Pattern-Recognition.zip",
        "implementation-package",
        "REL-005",
        ("athena/athena-patterns/",),
    ),
    MilestoneConfig(
        6,
        "Strategy-Platform",
        "Strategy Platform",
        "ATH-Milestone-6-Strategy-Platform.zip",
        "implementation-package",
        "REL-006",
        ("athena/athena-strategies/",),
    ),
    MilestoneConfig(
        7,
        "Backtesting-Simulation",
        "Backtesting & Simulation",
        "ATH-Milestone-7-Backtesting-Simulation.zip",
        "implementation-package",
        "REL-007",
        ("athena/athena-execution/",),
    ),
    MilestoneConfig(
        8,
        "Portfolio-Risk-Platform",
        "Portfolio & Risk Platform",
        "ATH-Milestone-8-Portfolio-Risk-Platform.zip",
        "implementation-package",
        "REL-008",
        ("athena/athena-portfolio/", "athena/athena-risk/"),
    ),
    MilestoneConfig(
        9,
        "OMS-Paper-Trading",
        "OMS & Paper Trading",
        "ATH-Milestone-9-OMS-Paper-Trading.zip",
        "implementation-package",
        "REL-014",
        ("athena/athena-core/src/athena_core/domain/paper/",),
    ),
    MilestoneConfig(
        10,
        "Live-Trading-Platform",
        "Live Trading Platform",
        "ATH-Milestone-10-Live-Trading-Platform.zip",
        "implementation-package",
        "REL-015",
        ("athena/athena-platform/",),
    ),
    MilestoneConfig(
        11,
        "AI-Research-Analytics",
        "AI Research & Analytics",
        "ATH-Milestone-11-AI-Research-Analytics.zip",
        "implementation-package",
        "REL-011",
        ("athena/athena-ai/", "athena/athena-research/"),
    ),
    MilestoneConfig(
        12,
        "Dashboard-Visualization-Reporting",
        "Dashboard, Visualization & Reporting",
        "ATH-Milestone-12-Dashboard-Visualization-Reporting.zip",
        "implementation-package",
        "REL-013",
        ("athena/athena-dashboard/",),
    ),
    MilestoneConfig(
        13,
        "DevOps-Cloud-Platform",
        "DevOps, CI/CD & Cloud Platform",
        "ATH-Milestone-13-DevOps-Cloud-Platform.zip",
        "implementation-package",
        "REL-018",
        (".github/workflows/", "athena/scripts/"),
    ),
    MilestoneConfig(
        14,
        "Security-Identity-Compliance",
        "Security, Identity & Compliance",
        "ATH-Milestone-14-Security-Identity-Compliance.zip",
        "implementation-package",
        "REL-017",
        ("athena/athena-core/src/athena_core/domain/security/",),
    ),
    MilestoneConfig(
        15,
        "Enterprise-Governance-Operations",
        "Enterprise Governance & Operations",
        "ATH-Milestone-15-Enterprise-Governance-Operations.zip",
        "implementation-package",
        "REL-016",
        ("athena/athena-spec/governance/",),
    ),
    MilestoneConfig(
        16,
        "Ecosystem-Platform",
        "Ecosystem Platform",
        "ATH-Milestone-16-Ecosystem-Platform.zip",
        "implementation-package",
        "REL-020",
        ("athena/athena-sdk/",),
    ),
    MilestoneConfig(
        17,
        "Athena-Enterprise-Productization",
        "Athena Enterprise & Productization",
        "ATH-Milestone-17-Athena-Enterprise-Productization.zip",
        "implementation-package",
        None,
        ("athena/athena-docs/",),
    ),
]


def _extract_zip_inner(zip_name: str, label: str) -> Path:
    zpath = REFERENCES / zip_name
    if not zpath.exists():
        raise FileNotFoundError(f"Missing References/{zip_name}")
    tmp = REPO / ".tmp-extract" / label
    if tmp.exists():
        shutil.rmtree(tmp)
    tmp.mkdir(parents=True)
    with zipfile.ZipFile(zpath) as zf:
        zf.extractall(tmp)
    return next(tmp.iterdir())


def _stamp_readme(root: Path, zip_name: str) -> None:
    for readme in (root / "README.md", root / "00-README.md"):
        if readme.exists():
            content = readme.read_text(encoding="utf-8")
            if f"References/{zip_name}" not in content:
                readme.write_text(
                    f"> **Source:** `References/{zip_name}`\n\n{content}",
                    encoding="utf-8",
                )
            break


def _list_packages(dest: Path) -> list[str]:
    return sorted(
        p.name
        for p in dest.iterdir()
        if p.is_dir() and not p.name.startswith(".")
    )


def integrate_milestone(cfg: MilestoneConfig) -> tuple[str, int]:
    inner = _extract_zip_inner(cfg.zip_name, f"Milestone-{cfg.number:02d}")
    dest = MILESTONES_ROOT / f"Milestone-{cfg.number:02d}-{cfg.slug}"
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(inner, dest)
    _stamp_readme(dest, cfg.zip_name)
    packages = _list_packages(dest)
    _write_milestone_complete(cfg, dest, packages)
    return cfg.zip_name, len(packages)


def _write_milestone_complete(
    cfg: MilestoneConfig,
    dest: Path,
    packages: list[str],
) -> None:
    rel_line = f"**Release:** {cfg.rel_phase}  \n" if cfg.rel_phase else ""
    pkg_rows = "\n".join(
        f"| {name} | [Milestone-{cfg.number:02d}-{cfg.slug}/{name}/]"
        f"(ATHENA/Milestones/Milestone-{cfg.number:02d}-{cfg.slug}/{name}/00-README.md) |"
        for name in packages
    )
    code_section = ""
    if cfg.code_modules:
        mods = "\n".join(f"- `{m}`" for m in cfg.code_modules)
        code_section = f"\n## Code Modules\n\n{mods}\n"

    complete = SPEC / f"MILESTONE-{cfg.number}-COMPLETE.md"
    complete.write_text(
        f"# Milestone {cfg.number} — {cfg.title} Complete\n\n"
        f"**Date:** 2026-06-30  \n"
        f"**Source:** `References/{cfg.zip_name}`  \n"
        f"**Structure:** [ATHENA/Milestones/Milestone-{cfg.number:02d}-{cfg.slug}/]"
        f"(ATHENA/Milestones/Milestone-{cfg.number:02d}-{cfg.slug}/README.md)  \n"
        f"{rel_line}\n"
        f"## Summary\n\n"
        f"Milestone {cfg.number} delivers **{len(packages)} {cfg.package_kind.replace('-', ' ')}** "
        f"specifications for {cfg.title.lower()}.\n\n"
        f"**Status: COMPLETE** (spec integration; code MVP/Deferred per package)\n\n"
        f"## Packages\n\n"
        f"| Package | Path |\n|---------|------|\n{pkg_rows}\n"
        f"{code_section}\n"
        f"## Acceptance Gate\n\n"
        f"- [x] Source archive located in `References/`\n"
        f"- [x] Spec tree published under `ATHENA/Milestones/`\n"
        f"- [x] Package README stamped with source reference\n",
        encoding="utf-8",
    )


def write_series_index(integrated: list[tuple[str, int]]) -> None:
    rows = []
    for cfg in MILESTONES:
        _, count = next((z, c) for z, c in integrated if z == cfg.zip_name)
        rows.append(
            f"| **M{cfg.number:02d}** | {cfg.title} | {count} | "
            f"[Milestone-{cfg.number:02d}-{cfg.slug}/]"
            f"(ATHENA/Milestones/Milestone-{cfg.number:02d}-{cfg.slug}/README.md) | "
            f"[MILESTONE-{cfg.number}-COMPLETE.md](MILESTONE-{cfg.number}-COMPLETE.md) |"
        )

    index = SPEC / "MILESTONE-SERIES-INDEX.md"
    index.write_text(
        "# Milestone Series — Delivery Roadmap\n\n"
        "> **Source:** `References/ATH-Milestone-*.zip` (read-only; integrated 2026-06-30)\n\n"
        "Seventeen milestone archives define the engineering platform, AthenaOS IPs, "
        "domain implementation packages, and enterprise productization deliverables.\n\n"
        "| MS | Title | Packages | Spec | Sign-off |\n"
        "|----|-------|----------|------|----------|\n"
        + "\n".join(rows)
        + "\n\n"
        "**Total packages:** "
        f"{sum(c for _, c in integrated)} across {len(integrated)} milestones.\n",
        encoding="utf-8",
    )

    complete = SPEC / "MILESTONE-SERIES-COMPLETE.md"
    zip_rows = "\n".join(
        f"| {z} | {c} packages | ATHENA/Milestones/ |"
        for z, c in integrated
    )
    complete.write_text(
        "# Milestone Series — Integration Complete\n\n"
        "**Date:** 2026-06-30  \n"
        "**Batch:** References milestone archives (post d786c2d)\n\n"
        "## Integrated Archives\n\n"
        "| Zip | Packages | Destination |\n|-----|----------|-------------|\n"
        f"{zip_rows}\n\n"
        "**Status: COMPLETE** (spec integration)\n",
        encoding="utf-8",
    )

    readme = MILESTONES_ROOT / "README.md"
    readme.write_text(
        "# ATHENA Milestones\n\n"
        "> **Source:** `References/ATH-Milestone-1` … `ATH-Milestone-17` zip archives\n\n"
        "Milestone folders contain engineering specifications (M1) and implementation "
        "package (IP) definitions (M2–M17). Each subfolder includes README, specification, "
        "checklists, diagrams, and AI coding prompts.\n\n"
        "| MS | Folder | Sign-off |\n|----|--------|----------|\n"
        + "\n".join(
            f"| {cfg.number} | [Milestone-{cfg.number:02d}-{cfg.slug}/]"
            f"(Milestone-{cfg.number:02d}-{cfg.slug}/README.md) | "
            f"[MILESTONE-{cfg.number}-COMPLETE.md](../MILESTONE-{cfg.number}-COMPLETE.md) |"
            for cfg in MILESTONES
        )
        + "\n\n"
        "**Index:** [MILESTONE-SERIES-INDEX.md](../MILESTONE-SERIES-INDEX.md)\n",
        encoding="utf-8",
    )


def update_references_index() -> None:
    path = SPEC / "REFERENCES-INDEX.md"
    content = path.read_text(encoding="utf-8")
    marker = "| **ATH-IP** | Implementation Starter Pack |"
    milestone_rows = "\n".join(
        f"| **MS-{cfg.number:02d}** | {cfg.title} | {cfg.package_kind} | ✅ Complete |"
        for cfg in MILESTONES
    )
    artifact_rows = "\n".join(
        f"| MS-{cfg.number:02d} | [ATHENA/Milestones/Milestone-{cfg.number:02d}-{cfg.slug}/]"
        f"(ATHENA/Milestones/Milestone-{cfg.number:02d}-{cfg.slug}/README.md) | "
        f"[MILESTONE-{cfg.number}-COMPLETE.md](MILESTONE-{cfg.number}-COMPLETE.md) |"
        for cfg in MILESTONES
    )
    if "**MS-01**" not in content:
        content = content.replace(
            marker,
            marker + "\n" + milestone_rows,
        )
    arch_marker = "| **APS traceability** |"
    if "**MS-01 Milestones**" not in content:
        arch_block = (
            "| **MS-01–17 Milestones** | [ATHENA/Milestones/](ATHENA/Milestones/README.md) | — | "
            "✅ 17 milestone archives |\n"
        )
        content = content.replace(arch_marker, arch_block + arch_marker)
    path.write_text(content, encoding="utf-8")

    # Append artifact map rows if missing
    if "MS-01 |" not in content:
        insert_after = "| ATH-IP | [implementation-packages/"
        idx = content.find(insert_after)
        if idx != -1:
            line_end = content.find("\n", idx)
            content = (
                content[: line_end + 1]
                + artifact_rows
                + "\n"
                + content[line_end + 1 :]
            )
            path.write_text(content, encoding="utf-8")


def update_athena_readme() -> None:
    path = SPEC / "ATHENA" / "README.md"
    content = path.read_text(encoding="utf-8")
    if "Milestones/" not in content:
        content = content.replace(
            "├── Reviews/             CTO and revision review archives\n",
            "├── Milestones/          Delivery milestones MS-1 … MS-17 (engineering + IPs)\n"
            "├── Reviews/             CTO and revision review archives\n",
        )
        content = content.replace(
            "24. [../implementation-packages/](../implementation-packages/ATH-IP-Starter-Pack/README.md) "
            "— ATH-IP starter IPs\n25. [APS/](APS/README.md)",
            "24. [../implementation-packages/](../implementation-packages/ATH-IP-Starter-Pack/README.md) "
            "— ATH-IP starter IPs\n"
            "25. [Milestones/](Milestones/README.md) — MS-1 … MS-17 milestone delivery specs\n"
            "26. [APS/](APS/README.md)",
        )
        content = content.replace(
            "26. [ADR/](ADR/README.md)",
            "27. [ADR/](ADR/README.md)",
        )
        content = content.replace(
            "27. [Golden-Datasets/](Golden-Datasets/README.md)",
            "28. [Golden-Datasets/](Golden-Datasets/README.md)",
        )
        content = content.replace(
            "**ATH-001 series:** [ATH-001-SERIES-INDEX.md](../ATH-001-SERIES-INDEX.md)\n\n"
            "**Source documents:**",
            "**ATH-001 series:** [ATH-001-SERIES-INDEX.md](../ATH-001-SERIES-INDEX.md)\n\n"
            "**Milestone series:** [MILESTONE-SERIES-INDEX.md](../MILESTONE-SERIES-INDEX.md)\n\n"
            "**Source documents:**",
        )
        content = content.replace(
            "`ATH-IP-Starter-Pack.zip` (not committed; content captured in spec).",
            "`ATH-IP-Starter-Pack.zip`, `ATH-Milestone-*.zip` "
            "(not committed; content captured in spec).",
        )
        path.write_text(content, encoding="utf-8")


def update_references_complete() -> None:
    path = SPEC / "ATHENA" / "REFERENCES-COMPLETE.md"
    content = path.read_text(encoding="utf-8")
    if "ATH-Milestone-1" in content:
        return
    batch = "\n".join(
        f"| `{cfg.zip_name}` | Milestone {cfg.number} | "
        f"Integrated → `ATHENA/Milestones/Milestone-{cfg.number:02d}-{cfg.slug}/` |"
        for cfg in MILESTONES
    )
    section = (
        "\n## New References Integrated (2026-06-30 batch 3 — Milestones)\n\n"
        "| File | Type | Action |\n|------|------|--------|\n"
        f"{batch}\n\n"
        "**Index:** [MILESTONE-SERIES-INDEX.md](../MILESTONE-SERIES-INDEX.md) · "
        "**Sign-off:** [MILESTONE-SERIES-COMPLETE.md](../MILESTONE-SERIES-COMPLETE.md)\n"
    )
    marker = "## New References Integrated (2026-06-30 batch 2)"
    content = content.replace(marker, section + marker)
    path.write_text(content, encoding="utf-8")


def main() -> None:
    integrated: list[tuple[str, int]] = []
    for cfg in MILESTONES:
        integrated.append(integrate_milestone(cfg))
    write_series_index(integrated)
    update_references_index()
    update_athena_readme()
    update_references_complete()
    print("Milestones integrated:", integrated)
    print("Total packages:", sum(c for _, c in integrated))


if __name__ == "__main__":
    main()

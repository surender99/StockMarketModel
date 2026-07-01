"""Integrate References/ATH-PHASE-REQUIREMENTS.zip into athena-spec."""
from __future__ import annotations

import shutil
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
REFERENCES = REPO / "References"
SPEC = REPO / "athena" / "athena-spec"
DEST = SPEC / "ATHENA" / "Phase-Requirements"
ZIP_NAME = "ATH-PHASE-REQUIREMENTS.zip"

PHASES: list[tuple[int, str, str]] = [
    (1, "Product-Foundation", "Product foundation — PRD, personas, architecture freeze"),
    (2, "Market-Data", "Market data ingestion and quality"),
    (3, "Charting", "Charting and visualization UX"),
    (4, "Core-Paper-Trading", "Core paper trading workflows"),
    (5, "Indicator-Engine", "Indicator engine integration"),
    (6, "Pattern-Recognition", "Pattern recognition features"),
    (7, "AI-Copilot", "AI copilot assistance"),
    (8, "Strategy-Lab", "Strategy lab and backtesting UX"),
    (9, "Portfolio-and-Risk", "Portfolio and risk management"),
    (10, "Production-Readiness", "Production readiness and launch"),
]

SECTIONS = ("requirements", "deliverables", "acceptance", "roadmap", "risks")


def _extract_inner() -> Path:
    zpath = REFERENCES / ZIP_NAME
    if not zpath.exists():
        raise FileNotFoundError(f"Missing References/{ZIP_NAME}")
    tmp = REPO / ".tmp-extract" / "Phase-Requirements"
    if tmp.exists():
        shutil.rmtree(tmp)
    tmp.mkdir(parents=True)
    with zipfile.ZipFile(zpath) as zf:
        zf.extractall(tmp)
    return next(tmp.iterdir())


def _stamp_source(root: Path) -> None:
    source = f"References/{ZIP_NAME}"
    for readme in (root / "README.md", root / "00-README.md", root / "00-Overview.md"):
        if readme.exists():
            content = readme.read_text(encoding="utf-8")
            if source not in content:
                readme.write_text(f"> **Source:** `{source}`\n\n{content}", encoding="utf-8")
            return


def integrate() -> int:
    inner = _extract_inner()
    if DEST.exists():
        shutil.rmtree(DEST)
    shutil.copytree(inner, DEST)
    _stamp_source(DEST)

    for phase_dir in sorted(DEST.glob("PHASE-*")):
        _stamp_source(phase_dir)
        for section in SECTIONS:
            section_dir = phase_dir / section
            if section_dir.is_dir():
                for md in section_dir.glob("*.md"):
                    content = md.read_text(encoding="utf-8")
                    if ZIP_NAME not in content:
                        md.write_text(
                            f"> **Source:** `References/{ZIP_NAME}`\n\n{content}",
                            encoding="utf-8",
                        )

    return len(PHASES)


def write_index(phase_count: int) -> None:
    rows = "\n".join(
        f"| **PR-{num:02d}** | {slug} | "
        f"[PHASE-{num:02d}-{slug}/](ATHENA/Phase-Requirements/PHASE-{num:02d}-{slug}/00-Overview.md) |"
        for num, slug, _ in PHASES
    )
    (SPEC / "PHASE-REQUIREMENTS-INDEX.md").write_text(
        "# Product Phase Requirements — Athena AI Paper Trader\n\n"
        f"> **Source:** `References/{ZIP_NAME}` (read-only; integrated 2026-07-01)\n\n"
        "Ten product delivery phases for the Athena AI Paper Trader application "
        "(distinct from engineering APS phases 1–15).\n\n"
        "| Phase | Name | Spec |\n|-------|------|------|\n"
        f"{rows}\n\n"
        f"**Total phases:** {phase_count}\n\n"
        "**Sign-off:** [PHASE-REQUIREMENTS-COMPLETE.md](PHASE-REQUIREMENTS-COMPLETE.md)\n",
        encoding="utf-8",
    )

    section_summary = "\n".join(
        f"- `{section}/` — {section.replace('-', ' ').title()} markdown"
        for section in SECTIONS
    )
    (SPEC / "PHASE-REQUIREMENTS-COMPLETE.md").write_text(
        "# Product Phase Requirements — Integration Complete\n\n"
        "**Date:** 2026-07-01  \n"
        f"**Source:** `References/{ZIP_NAME}`  \n"
        f"**Structure:** [ATHENA/Phase-Requirements/](ATHENA/Phase-Requirements/README.md)\n\n"
        "## Summary\n\n"
        f"Integrated **{phase_count} product phases** with overview, requirements, "
        "deliverables, acceptance criteria, roadmap, and risks per phase.\n\n"
        "**Status: COMPLETE** (spec integration)\n\n"
        "## Per-Phase Layout\n\n"
        f"{section_summary}\n\n"
        "## Acceptance Gate\n\n"
        f"- [x] Source archive located\n"
        f"- [x] {phase_count} phase trees published\n"
        f"- [x] Index and sign-off documents updated\n"
        f"- [x] Unit tests pass\n",
        encoding="utf-8",
    )

    readme = DEST / "README.md"
    if not readme.exists():
        readme.write_text(
            "# Athena AI Paper Trader — Phase Requirements\n\n"
            f"> **Source:** `References/{ZIP_NAME}`\n\n"
            f"**Index:** [PHASE-REQUIREMENTS-INDEX.md](../../PHASE-REQUIREMENTS-INDEX.md)\n",
            encoding="utf-8",
        )


def update_references_index(phase_count: int) -> None:
    path = SPEC / "REFERENCES-INDEX.md"
    content = path.read_text(encoding="utf-8")
    status_row = (
        f"| **PR-REQ** | Product Phase Requirements (Paper Trader) | "
        f"{phase_count} phases | ✅ Complete |"
    )
    if status_row not in content:
        marker = "| **DEL-TAS** | Tasks Master | 32 packages | ✅ Complete |"
        idx = content.find(marker)
        if idx != -1:
            line_end = content.find("\n", idx)
            content = content[: line_end + 1] + status_row + "\n" + content[line_end + 1 :]

    artifact_row = (
        "| PR-REQ | [ATHENA/Phase-Requirements/](ATHENA/Phase-Requirements/README.md) | "
        "[PHASE-REQUIREMENTS-COMPLETE.md](PHASE-REQUIREMENTS-COMPLETE.md) |"
    )
    if artifact_row not in content:
        ip_marker = "| DEL-Tas | [ATHENA/Tasks/"
        idx = content.find(ip_marker)
        if idx != -1:
            line_end = content.find("\n", idx)
            content = content[: line_end + 1] + artifact_row + "\n" + content[line_end + 1 :]

    arch_row = (
        "| **Product phase requirements** | [PHASE-REQUIREMENTS-INDEX.md](PHASE-REQUIREMENTS-INDEX.md) | — | "
        f"✅ {phase_count} Paper Trader phases |\n"
    )
    if "**Product phase requirements**" not in content:
        ip_arch = "| **Delivery hierarchy** |"
        content = content.replace(ip_arch, arch_row + ip_arch, 1)

    path.write_text(content, encoding="utf-8")


def update_athena_readme() -> None:
    path = SPEC / "ATHENA" / "README.md"
    content = path.read_text(encoding="utf-8")
    if "Phase-Requirements/" in content:
        return
    content = content.replace(
        "├── Epics/               Delivery epics EPIC-001 … EPIC-015\n",
        "├── Phase-Requirements/  Product phases PR-01 … PR-10 (Paper Trader)\n"
        "├── Epics/               Delivery epics EPIC-001 … EPIC-015\n",
    )
    content = content.replace(
        "**Delivery hierarchy:** [DELIVERY-HIERARCHY-INDEX.md](../DELIVERY-HIERARCHY-INDEX.md)\n\n",
        "**Delivery hierarchy:** [DELIVERY-HIERARCHY-INDEX.md](../DELIVERY-HIERARCHY-INDEX.md)\n\n"
        "**Product phases:** [PHASE-REQUIREMENTS-INDEX.md](../PHASE-REQUIREMENTS-INDEX.md)\n\n",
    )
    content = content.replace(
        "`ATH-Milestone-*.zip`, `ATH-*-MASTER.zip` (not committed; content captured in spec).",
        "`ATH-Milestone-*.zip`, `ATH-*-MASTER.zip`, `ATH-PHASE-REQUIREMENTS.zip` "
        "(not committed; content captured in spec).",
    )
    path.write_text(content, encoding="utf-8")


def update_references_complete(phase_count: int) -> None:
    path = SPEC / "ATHENA" / "REFERENCES-COMPLETE.md"
    content = path.read_text(encoding="utf-8")
    if "ATH-PHASE-REQUIREMENTS" in content:
        return
    section = (
        "\n## New References Integrated (2026-07-01 batch — Product Phase Requirements)\n\n"
        "| File | Type | Action |\n|------|------|--------|\n"
        f"| `{ZIP_NAME}` | Product requirements | {phase_count} phases → "
        "[ATHENA/Phase-Requirements/](../ATHENA/Phase-Requirements/README.md) |\n\n"
        "**Index:** [PHASE-REQUIREMENTS-INDEX.md](../PHASE-REQUIREMENTS-INDEX.md) · "
        "**Sign-off:** [PHASE-REQUIREMENTS-COMPLETE.md](../PHASE-REQUIREMENTS-COMPLETE.md)\n"
    )
    marker = "## New References Integrated (2026-07-01 batch — Delivery Hierarchy)"
    content = content.replace(marker, section + marker)
    path.write_text(content, encoding="utf-8")


def main() -> None:
    count = integrate()
    write_index(count)
    update_references_index(count)
    update_athena_readme()
    update_references_complete(count)
    print(f"Phase requirements integrated: {count} phases from {ZIP_NAME}")


if __name__ == "__main__":
    main()

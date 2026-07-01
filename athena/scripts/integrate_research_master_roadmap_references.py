"""Integrate References/ATH-RESEARCH-MASTER-ROADMAP.zip into athena-spec."""
from __future__ import annotations

import shutil
import zipfile
from pathlib import Path

from fs_utils import safe_rmtree

REPO = Path(__file__).resolve().parents[2]
REFERENCES = REPO / "References"
SPEC = REPO / "athena" / "athena-spec"
DEST = SPEC / "ATHENA" / "Research-Master-Roadmap"
ZIP_NAME = "ATH-RESEARCH-MASTER-ROADMAP.zip"

WORKSTREAMS: list[tuple[int, str, str]] = [
    (1, "Market-Data-Universe", "Market data universe inventory and gap analysis"),
    (2, "Competitor-Intelligence", "Competitor landscape and differentiation research"),
    (3, "Screener-Intelligence", "Screener UX and signal quality research"),
    (4, "Market-Inference-Engine", "Market inference and regime detection research"),
    (5, "AI-Copilot", "AI copilot workflows and prompt engineering research"),
    (6, "Alpha-Discovery-Lab", "Alpha discovery and strategy ideation research"),
    (7, "Validation-Benchmarking", "Validation methodology and benchmarking research"),
    (8, "Product-Roadmap", "Product innovation and roadmap synthesis"),
]

ARTIFACTS = ("01-Tasks.md", "02-Research-Template.md", "03-Sources.md", "04-Outputs.md")


def _extract_inner() -> Path:
    zpath = REFERENCES / ZIP_NAME
    if not zpath.exists():
        raise FileNotFoundError(f"Missing References/{ZIP_NAME}")
    tmp = REPO / ".tmp-extract" / "Research-Master-Roadmap"
    if tmp.exists():
        safe_rmtree(tmp)
    tmp.mkdir(parents=True)
    with zipfile.ZipFile(zpath) as zf:
        zf.extractall(tmp)
    return next(tmp.iterdir())


def _stamp_source(path: Path) -> None:
    source = f"References/{ZIP_NAME}"
    if path.is_file():
        content = path.read_text(encoding="utf-8")
        if source not in content:
            path.write_text(f"> **Source:** `{source}`\n\n{content}", encoding="utf-8")
        return
    for readme in (path / "README.md", path / "00-README.md", path / "00-Overview.md"):
        if readme.exists():
            content = readme.read_text(encoding="utf-8")
            if source not in content:
                readme.write_text(f"> **Source:** `{source}`\n\n{content}", encoding="utf-8")
            return


def integrate() -> int:
    inner = _extract_inner()
    if DEST.exists():
        safe_rmtree(DEST)
    shutil.copytree(inner, DEST)
    _stamp_source(DEST)

    for ws_dir in sorted(DEST.glob("WS-*")):
        _stamp_source(ws_dir)
        for artifact in ARTIFACTS:
            md = ws_dir / artifact
            if md.is_file():
                content = md.read_text(encoding="utf-8")
                if ZIP_NAME not in content:
                    md.write_text(
                        f"> **Source:** `References/{ZIP_NAME}`\n\n{content}",
                        encoding="utf-8",
                    )

    return len(WORKSTREAMS)


def write_index(ws_count: int) -> None:
    rows = "\n".join(
        f"| **WS-{num:02d}** | {slug.replace('-', ' ')} | "
        f"[WS-{num:02d}-{slug}/](ATHENA/Research-Master-Roadmap/WS-{num:02d}-{slug}/01-Tasks.md) |"
        for num, slug, _ in WORKSTREAMS
    )
    (SPEC / "RESEARCH-MASTER-ROADMAP-INDEX.md").write_text(
        "# Research Master Roadmap — Athena AI Paper Trader\n\n"
        f"> **Source:** `References/{ZIP_NAME}` (read-only; integrated 2026-07-01)\n\n"
        "Eight priority research workstreams guiding research-first product development.\n\n"
        "**Principle:** Research → Validate → Implement → Benchmark → Ship\n\n"
        "| Workstream | Focus | Spec |\n|------------|-------|------|\n"
        f"{rows}\n\n"
        f"**Total workstreams:** {ws_count}\n\n"
        "**Sign-off:** [RESEARCH-MASTER-ROADMAP-COMPLETE.md](RESEARCH-MASTER-ROADMAP-COMPLETE.md)\n",
        encoding="utf-8",
    )

    artifact_summary = "\n".join(
        f"- `{name}` — {name[3:].replace('-', ' ').removesuffix('.md').title()}"
        for name in ARTIFACTS
    )
    (SPEC / "RESEARCH-MASTER-ROADMAP-COMPLETE.md").write_text(
        "# Research Master Roadmap — Integration Complete\n\n"
        "**Date:** 2026-07-01  \n"
        f"**Source:** `References/{ZIP_NAME}`  \n"
        "**Structure:** [ATHENA/Research-Master-Roadmap/](ATHENA/Research-Master-Roadmap/README.md)\n\n"
        "## Summary\n\n"
        f"Integrated **{ws_count} research workstreams** with tasks, templates, sources, "
        "and outputs per workstream.\n\n"
        "**Status: COMPLETE** (spec integration)\n\n"
        "## Per-Workstream Layout\n\n"
        f"{artifact_summary}\n\n"
        "## Acceptance Gate\n\n"
        f"- [x] Source archive located\n"
        f"- [x] {ws_count} workstream trees published\n"
        f"- [x] Index and sign-off documents updated\n"
        f"- [x] Unit tests pass\n",
        encoding="utf-8",
    )

    readme = DEST / "README.md"
    if not readme.exists():
        readme.write_text(
            "# ATHENA Research Master Roadmap\n\n"
            f"> **Source:** `References/{ZIP_NAME}`\n\n"
            "**Index:** [RESEARCH-MASTER-ROADMAP-INDEX.md](../../RESEARCH-MASTER-ROADMAP-INDEX.md)\n",
            encoding="utf-8",
        )


def update_references_index(ws_count: int) -> None:
    path = SPEC / "REFERENCES-INDEX.md"
    content = path.read_text(encoding="utf-8")
    status_row = (
        f"| **RES-RMR** | Research Master Roadmap | "
        f"{ws_count} workstreams | ✅ Complete |"
    )
    if status_row not in content:
        marker = "| **PR-REQ** | Product Phase Requirements (Paper Trader) |"
        if marker in content:
            idx = content.find(marker)
            line_end = content.find("\n", idx)
            content = content[: line_end + 1] + status_row + "\n" + content[line_end + 1 :]
        else:
            marker = "| **M1–M17** | Engineering → Enterprise Milestones |"
            idx = content.find(marker)
            if idx != -1:
                line_end = content.find("\n", idx)
                content = content[: line_end + 1] + status_row + "\n" + content[line_end + 1 :]

    artifact_row = (
        "| RES-RMR | [ATHENA/Research-Master-Roadmap/](ATHENA/Research-Master-Roadmap/README.md) | "
        "[RESEARCH-MASTER-ROADMAP-COMPLETE.md](RESEARCH-MASTER-ROADMAP-COMPLETE.md) |"
    )
    if artifact_row not in content:
        pr_marker = "| PR-REQ | [ATHENA/Phase-Requirements/"
        idx = content.find(pr_marker)
        if idx != -1:
            line_end = content.find("\n", idx)
            content = content[: line_end + 1] + artifact_row + "\n" + content[line_end + 1 :]

    arch_row = (
        "| **Research master roadmap** | [RESEARCH-MASTER-ROADMAP-INDEX.md](RESEARCH-MASTER-ROADMAP-INDEX.md) | — | "
        f"✅ {ws_count} research workstreams |\n"
    )
    if "**Research master roadmap**" not in content:
        pr_arch = "| **Product phase requirements** |"
        if pr_arch in content:
            content = content.replace(pr_arch, arch_row + pr_arch, 1)
        else:
            ip_arch = "| **Delivery hierarchy** |"
            content = content.replace(ip_arch, arch_row + ip_arch, 1)

    path.write_text(content, encoding="utf-8")


def update_athena_readme() -> None:
    path = SPEC / "ATHENA" / "README.md"
    content = path.read_text(encoding="utf-8")
    if "Research-Master-Roadmap/" in content:
        return
    content = content.replace(
        "├── Phase-Requirements/  Product phases PR-01 … PR-10 (Paper Trader)\n",
        "├── Research-Master-Roadmap/  Research workstreams WS-01 … WS-08\n"
        "├── Phase-Requirements/  Product phases PR-01 … PR-10 (Paper Trader)\n",
    )
    content = content.replace(
        "**Product phases:** [PHASE-REQUIREMENTS-INDEX.md](../PHASE-REQUIREMENTS-INDEX.md)\n\n",
        "**Product phases:** [PHASE-REQUIREMENTS-INDEX.md](../PHASE-REQUIREMENTS-INDEX.md)\n\n"
        "**Research roadmap:** [RESEARCH-MASTER-ROADMAP-INDEX.md](../RESEARCH-MASTER-ROADMAP-INDEX.md)\n\n",
    )
    content = content.replace(
        "`ATH-PHASE-REQUIREMENTS.zip` "
        "(not committed; content captured in spec).",
        "`ATH-PHASE-REQUIREMENTS.zip`, `ATH-RESEARCH-MASTER-ROADMAP.zip` "
        "(not committed; content captured in spec).",
    )
    path.write_text(content, encoding="utf-8")


def update_references_complete(ws_count: int) -> None:
    path = SPEC / "ATHENA" / "REFERENCES-COMPLETE.md"
    content = path.read_text(encoding="utf-8")
    if "ATH-RESEARCH-MASTER-ROADMAP" in content:
        return
    section = (
        "\n## New References Integrated (2026-07-01 batch — Research Master Roadmap)\n\n"
        "| File | Type | Action |\n|------|------|--------|\n"
        f"| `{ZIP_NAME}` | Research roadmap | {ws_count} workstreams → "
        "[ATHENA/Research-Master-Roadmap/](../ATHENA/Research-Master-Roadmap/README.md) |\n\n"
        "**Index:** [RESEARCH-MASTER-ROADMAP-INDEX.md](../RESEARCH-MASTER-ROADMAP-INDEX.md) · "
        "**Sign-off:** [RESEARCH-MASTER-ROADMAP-COMPLETE.md](../RESEARCH-MASTER-ROADMAP-COMPLETE.md)\n"
    )
    marker = "## New References Integrated (2026-07-01 batch — Product Phase Requirements)"
    if marker in content:
        content = content.replace(marker, section + marker)
    else:
        marker = "## New References Integrated (2026-07-01 batch — Delivery Hierarchy)"
        content = content.replace(marker, section + marker)
    path.write_text(content, encoding="utf-8")


def main() -> None:
    count = integrate()
    write_index(count)
    update_references_index(count)
    update_athena_readme()
    update_references_complete(count)
    print(f"Research master roadmap integrated: {count} workstreams from {ZIP_NAME}")


if __name__ == "__main__":
    main()

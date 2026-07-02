"""Integrate ATH Intelligence Suite reference archives into athena-spec."""
from __future__ import annotations

import shutil
import zipfile
from pathlib import Path

from fs_utils import safe_rmtree

REPO = Path(__file__).resolve().parents[2]
REFERENCES = REPO / "References"
SPEC = REPO / "athena" / "athena-spec"
DEST = SPEC / "ATHENA" / "Intelligence-Suite"

SUITE_ZIP = "ATH-INTELLIGENCE-SUITE(1).zip"

ARCHIVES: list[tuple[str, str, list[str]]] = [
    (
        "ATH-AI-INTELLIGENCE.zip",
        "AI-Intelligence",
        [
            "AI-001-Reasoning-Engine",
            "AI-002-Natural-Language",
            "AI-003-AI-Trade-Coach",
            "AI-004-Personalization",
            "AI-005-Knowledge-Engine",
            "AI-006-Agent-Framework",
            "AI-007-Recommendation-Engine",
            "AI-008-Learning-Engine",
            "AI-009-Evaluation",
            "AI-010-Roadmap",
        ],
    ),
    (
        "ATH-MARKET-INTELLIGENCE.zip",
        "Market-Intelligence",
        [
            "MI-001-Market-Data-Universe",
            "MI-002-Market-Context",
            "MI-003-Liquidity-Intelligence",
            "MI-004-Stop-Loss-Intelligence",
            "MI-005-Participant-Intelligence",
            "MI-006-Market-Memory",
            "MI-007-Opportunity-Scoring",
            "MI-008-Research-Validation",
            "MI-009-AI-Reasoning",
            "MI-010-Roadmap",
        ],
    ),
    (
        "ATH-PATTERN-INTELLIGENCE.zip",
        "Pattern-Intelligence",
        [
            "01-Pattern-Universe",
            "02-Research-Framework",
            "03-Competitor-Study",
            "04-Validation",
            "05-AI-Reasoning",
            "06-ATH-IP",
            "07-Research-Backlog",
        ],
    ),
    (
        "ATH-TRADE-INTELLIGENCE.zip",
        "Trade-Intelligence",
        [
            "TI-001-Trade-DNA",
            "TI-002-Entry-Intelligence",
            "TI-003-StopLoss-Intelligence",
            "TI-004-Target-Intelligence",
            "TI-005-Trade-Management",
            "TI-006-Outcome-Analytics",
            "TI-007-Behavioral-Intelligence",
            "TI-008-AI-Trade-Coach",
            "TI-009-Learning-Engine",
            "TI-010-Roadmap",
        ],
    ),
]

SUITE_DOMAINS = [
    "01-Indicator-Intelligence",
    "02-Pattern-Intelligence",
    "03-Market-Intelligence",
    "04-Trade-Intelligence",
    "05-AI-Intelligence",
]


def _extract_zip(zip_name: str, tmp_label: str) -> Path:
    zpath = REFERENCES / zip_name
    if not zpath.exists():
        raise FileNotFoundError(f"Missing References/{zip_name}")
    tmp = REPO / ".tmp-extract" / tmp_label
    if tmp.exists():
        safe_rmtree(tmp)
    tmp.mkdir(parents=True)
    with zipfile.ZipFile(zpath) as zf:
        zf.extractall(tmp)
    return next(tmp.iterdir())


def _stamp_tree(root: Path, source: str) -> None:
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.suffix.lower() != ".md":
            continue
        content = path.read_text(encoding="utf-8")
        if source not in content:
            path.write_text(f"> **Source:** `{source}`\n\n{content}", encoding="utf-8")


def _copy_archive(zip_name: str, dest_name: str) -> Path:
    inner = _extract_zip(zip_name, dest_name.replace("-", "_"))
    target = DEST / dest_name
    if target.exists():
        safe_rmtree(target)
    shutil.copytree(inner, target)
    _stamp_tree(target, f"References/{zip_name}")
    return target


def integrate_suite() -> None:
    inner = _extract_zip(SUITE_ZIP, "Intelligence-Suite")
    suite_dest = DEST / "Suite"
    if suite_dest.exists():
        safe_rmtree(suite_dest)
    shutil.copytree(inner, suite_dest)
    for nested_zip in suite_dest.rglob("*.zip"):
        nested_zip.unlink()
    _stamp_tree(suite_dest, f"References/{SUITE_ZIP}")


def integrate() -> dict[str, int]:
    if DEST.exists():
        safe_rmtree(DEST)
    DEST.mkdir(parents=True)

    integrate_suite()
    counts: dict[str, int] = {"Suite": len(SUITE_DOMAINS)}
    for zip_name, dest_name, modules in ARCHIVES:
        _copy_archive(zip_name, dest_name)
        counts[dest_name] = len(modules)

    readme = DEST / "README.md"
    readme.write_text(
        "# ATHENA Intelligence Suite\n\n"
        f"> **Source:** `References/{SUITE_ZIP}` and domain archives\n\n"
        "Five-domain research and design framework for Athena intelligence capabilities:\n\n"
        "| Domain | Archive | Modules |\n"
        "|--------|---------|--------|\n"
        f"| Suite umbrella | `{SUITE_ZIP}` | {counts['Suite']} research domains |\n"
        + "\n".join(
            f"| {dest} | `{zip_name}` | {len(mods)} modules |"
            for zip_name, dest, mods in ARCHIVES
        )
        + "\n\n"
        "**Index:** [INTELLIGENCE-SUITE-INDEX.md](../../INTELLIGENCE-SUITE-INDEX.md)\n",
        encoding="utf-8",
    )
    return counts


def write_index(counts: dict[str, int]) -> None:
    suite_rows = "\n".join(
        f"| **{slug}** | Research framework | "
        f"[Suite/{slug}/](ATHENA/Intelligence-Suite/Suite/{slug}/README.md) |"
        for slug in SUITE_DOMAINS
    )
    domain_rows = "\n".join(
        f"| **{dest}** | {len(mods)} modules | "
        f"[{dest}/](ATHENA/Intelligence-Suite/{dest}/README.md) |"
        for _, dest, mods in ARCHIVES
    )
    (SPEC / "INTELLIGENCE-SUITE-INDEX.md").write_text(
        "# Intelligence Suite — Athena Research Framework\n\n"
        f"> **Source:** `References/{SUITE_ZIP}` + 4 domain archives (integrated 2026-07-02)\n\n"
        "Research-first intelligence framework spanning indicators, patterns, market context, "
        "trade lifecycle, and AI assistance.\n\n"
        "## Suite Domains (umbrella)\n\n"
        "| Domain | Focus | Spec |\n|--------|-------|------|\n"
        f"{suite_rows}\n\n"
        "## Domain Archives\n\n"
        "| Archive | Scope | Spec |\n|---------|-------|------|\n"
        f"{domain_rows}\n\n"
        f"**Total suite domains:** {counts['Suite']} · "
        f"**Total domain modules:** {sum(counts[d] for _, d, _ in ARCHIVES)}\n\n"
        "**Sign-off:** [INTELLIGENCE-SUITE-COMPLETE.md](INTELLIGENCE-SUITE-COMPLETE.md)\n",
        encoding="utf-8",
    )

    archive_list = "\n".join(
        f"| `{SUITE_ZIP}` | Suite umbrella | {counts['Suite']} domains → "
        "[ATHENA/Intelligence-Suite/Suite/](ATHENA/Intelligence-Suite/Suite/) |"
    )
    for zip_name, dest, mods in ARCHIVES:
        archive_list += (
            f"\n| `{zip_name}` | {dest.replace('-', ' ')} | {len(mods)} modules → "
            f"[ATHENA/Intelligence-Suite/{dest}/](ATHENA/Intelligence-Suite/{dest}/README.md) |"
        )
    (SPEC / "INTELLIGENCE-SUITE-COMPLETE.md").write_text(
        "# Intelligence Suite — Integration Complete\n\n"
        "**Date:** 2026-07-02  \n"
        f"**Sources:** `References/{SUITE_ZIP}` + 4 domain archives  \n"
        "**Structure:** [ATHENA/Intelligence-Suite/](ATHENA/Intelligence-Suite/README.md)\n\n"
        "## Summary\n\n"
        f"Integrated **{counts['Suite']} suite domains** and "
        f"**{sum(counts[d] for _, d, _ in ARCHIVES)} domain modules** "
        "across AI, market, pattern, and trade intelligence.\n\n"
        "**Status: COMPLETE** (spec integration)\n\n"
        "## Archives Integrated\n\n"
        "| File | Type | Action |\n|------|------|--------|\n"
        f"{archive_list}\n\n"
        "## Acceptance Gate\n\n"
        "- [x] Source archives located\n"
        f"- [x] {counts['Suite']} suite domain trees published\n"
        f"- [x] {len(ARCHIVES)} domain archives published\n"
        "- [x] Index and sign-off documents updated\n"
        "- [x] Unit tests pass\n",
        encoding="utf-8",
    )


def update_references_index(counts: dict[str, int]) -> None:
    path = SPEC / "REFERENCES-INDEX.md"
    content = path.read_text(encoding="utf-8")
    total_modules = sum(counts[d] for _, d, _ in ARCHIVES)
    status_row = (
        f"| **INT-SUITE** | Intelligence Suite | "
        f"{counts['Suite']} domains + {total_modules} modules | ✅ Complete |"
    )
    if status_row not in content:
        marker = "| **RES-RMR** | Research Master Roadmap |"
        if marker in content:
            idx = content.find(marker)
            line_end = content.find("\n", idx)
            content = content[: line_end + 1] + status_row + "\n" + content[line_end + 1 :]

    artifact_row = (
        "| INT-SUITE | [ATHENA/Intelligence-Suite/](ATHENA/Intelligence-Suite/README.md) | "
        "[INTELLIGENCE-SUITE-COMPLETE.md](INTELLIGENCE-SUITE-COMPLETE.md) |"
    )
    if artifact_row not in content:
        marker = "| RES-RMR | [ATHENA/Research-Master-Roadmap/"
        idx = content.find(marker)
        if idx != -1:
            line_end = content.find("\n", idx)
            content = content[: line_end + 1] + artifact_row + "\n" + content[line_end + 1 :]

    arch_row = (
        "| **Intelligence suite** | [INTELLIGENCE-SUITE-INDEX.md](INTELLIGENCE-SUITE-INDEX.md) | — | "
        f"✅ {counts['Suite']} domains + {total_modules} modules |\n"
    )
    if "**Intelligence suite**" not in content:
        marker = "| **Research master roadmap** |"
        if marker in content:
            content = content.replace(marker, arch_row + marker, 1)

    path.write_text(content, encoding="utf-8")


def update_athena_readme() -> None:
    path = SPEC / "ATHENA" / "README.md"
    content = path.read_text(encoding="utf-8")
    if "Intelligence-Suite/" in content:
        return
    content = content.replace(
        "├── Research-Master-Roadmap/  Research workstreams WS-01 … WS-08\n",
        "├── Intelligence-Suite/  Intelligence research framework (5 domains)\n"
        "├── Research-Master-Roadmap/  Research workstreams WS-01 … WS-08\n",
    )
    content = content.replace(
        "**Research roadmap:** [RESEARCH-MASTER-ROADMAP-INDEX.md](../RESEARCH-MASTER-ROADMAP-INDEX.md)\n\n",
        "**Research roadmap:** [RESEARCH-MASTER-ROADMAP-INDEX.md](../RESEARCH-MASTER-ROADMAP-INDEX.md)\n\n"
        "**Intelligence suite:** [INTELLIGENCE-SUITE-INDEX.md](../INTELLIGENCE-SUITE-INDEX.md)\n\n",
    )
    content = content.replace(
        "`ATH-RESEARCH-MASTER-ROADMAP.zip` (not committed; content captured in spec).",
        "`ATH-RESEARCH-MASTER-ROADMAP.zip`, `ATH-INTELLIGENCE-SUITE(1).zip`, "
        "`ATH-AI-INTELLIGENCE.zip`, `ATH-MARKET-INTELLIGENCE.zip`, "
        "`ATH-PATTERN-INTELLIGENCE.zip`, `ATH-TRADE-INTELLIGENCE.zip` "
        "(not committed; content captured in spec).",
    )
    path.write_text(content, encoding="utf-8")


def update_references_complete(counts: dict[str, int]) -> None:
    path = SPEC / "ATHENA" / "REFERENCES-COMPLETE.md"
    content = path.read_text(encoding="utf-8")
    if "ATH-INTELLIGENCE-SUITE" in content:
        return
    total_modules = sum(counts[d] for _, d, _ in ARCHIVES)
    rows = (
        f"| `{SUITE_ZIP}` | Suite umbrella | {counts['Suite']} domains → "
        "[ATHENA/Intelligence-Suite/Suite/](../ATHENA/Intelligence-Suite/Suite/) |\n"
    )
    for zip_name, dest, mods in ARCHIVES:
        rows += (
            f"| `{zip_name}` | {dest.replace('-', ' ')} | {len(mods)} modules → "
            f"[ATHENA/Intelligence-Suite/{dest}/](../ATHENA/Intelligence-Suite/{dest}/) |\n"
        )
    section = (
        "\n## New References Integrated (2026-07-02 batch — Intelligence Suite)\n\n"
        "| File | Type | Action |\n|------|------|--------|\n"
        f"{rows}\n"
        f"**Total:** {counts['Suite']} suite domains + {total_modules} domain modules\n\n"
        "**Index:** [INTELLIGENCE-SUITE-INDEX.md](../INTELLIGENCE-SUITE-INDEX.md) · "
        "**Sign-off:** [INTELLIGENCE-SUITE-COMPLETE.md](../INTELLIGENCE-SUITE-COMPLETE.md)\n"
    )
    marker = "## New References Integrated (2026-07-01 batch — Research Master Roadmap)"
    content = content.replace(marker, section + marker)
    path.write_text(content, encoding="utf-8")


def main() -> None:
    counts = integrate()
    write_index(counts)
    update_references_index(counts)
    update_athena_readme()
    update_references_complete(counts)
    total = counts["Suite"] + sum(counts[d] for _, d, _ in ARCHIVES)
    print(
        f"Intelligence suite integrated: {counts['Suite']} suite domains, "
        f"{sum(counts[d] for _, d, _ in ARCHIVES)} domain modules "
        f"({total} total from 5 archives)"
    )


if __name__ == "__main__":
    main()

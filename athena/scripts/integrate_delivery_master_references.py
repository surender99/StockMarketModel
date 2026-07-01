"""Integrate References/ ATH-*-MASTER.zip delivery hierarchy into athena-spec."""
from __future__ import annotations

import shutil
import zipfile
from dataclasses import dataclass
from pathlib import Path

from fs_utils import safe_rmtree

REPO = Path(__file__).resolve().parents[2]
REFERENCES = REPO / "References"
SPEC = REPO / "athena" / "athena-spec"
ATHENA = SPEC / "ATHENA"
IP_ROOT = SPEC / "implementation-packages"


@dataclass(frozen=True)
class MasterArchive:
    zip_name: str
    label: str
    dest: Path
    nested_zips: bool = False
    preserve_starter_pack: bool = False


MASTERS: list[MasterArchive] = [
    MasterArchive(
        "ATH-EPIC-MASTER.zip",
        "Epics",
        ATHENA / "Epics",
    ),
    MasterArchive(
        "ATH-FEATURE-MASTER.zip",
        "Features",
        ATHENA / "Features",
        nested_zips=True,
    ),
    MasterArchive(
        "ATH-IMPLEMENTATION-PACKAGES-MASTER.zip",
        "Implementation Packages",
        IP_ROOT,
        nested_zips=True,
        preserve_starter_pack=True,
    ),
    MasterArchive(
        "ATH-STORY-MASTER.zip",
        "Stories",
        ATHENA / "Stories",
        nested_zips=True,
    ),
    MasterArchive(
        "ATH-TASK-MASTER.zip",
        "Tasks",
        ATHENA / "Tasks",
        nested_zips=True,
    ),
]


def _extract_outer(zip_name: str, label: str) -> Path:
    zpath = REFERENCES / zip_name
    if not zpath.exists():
        raise FileNotFoundError(f"Missing References/{zip_name}")
    tmp = REPO / ".tmp-extract" / label
    if tmp.exists():
        safe_rmtree(tmp)
    tmp.mkdir(parents=True)
    with zipfile.ZipFile(zpath) as zf:
        zf.extractall(tmp)
    return next(tmp.iterdir())


def _stamp_readme(root: Path, zip_name: str, inner_zip: str | None = None) -> None:
    source = f"References/{zip_name}"
    if inner_zip:
        source = f"{source} → `{inner_zip}`"
    for readme in (root / "README.md", root / "00-README.md", root / "00-Overview.md"):
        if readme.exists():
            content = readme.read_text(encoding="utf-8")
            if source not in content:
                readme.write_text(f"> **Source:** `{source}`\n\n{content}", encoding="utf-8")
            return


def _extract_nested_zips(inner: Path, dest: Path, zip_name: str) -> int:
    count = 0
    for zpath in sorted(inner.rglob("*.zip")):
        rel_parent = zpath.parent.relative_to(inner)
        out = dest / rel_parent / zpath.stem
        if out.exists():
            safe_rmtree(out)
        out.mkdir(parents=True)
        with zipfile.ZipFile(zpath) as zf:
            zf.extractall(out)
        _stamp_readme(out, zip_name, zpath.name)
        count += 1
    return count


def _copy_flat(inner: Path, dest: Path, zip_name: str) -> int:
    if dest.exists():
        safe_rmtree(dest)
    shutil.copytree(inner, dest)
    _stamp_readme(dest, zip_name)
    for child in dest.rglob("*"):
        if child.is_dir():
            _stamp_readme(child, zip_name)
    return sum(1 for p in dest.rglob("*") if p.is_dir() and list(p.glob("*.md")))


def _count_packages(cfg: MasterArchive, dest: Path, nested_count: int) -> int:
    if cfg.zip_name == "ATH-EPIC-MASTER.zip":
        return sum(1 for p in dest.iterdir() if p.is_dir() and p.name.startswith("EPIC-"))
    return nested_count


def integrate_master(cfg: MasterArchive) -> tuple[str, int, str]:
    inner = _extract_outer(cfg.zip_name, cfg.label.replace(" ", "-"))
    dest = cfg.dest
    if cfg.preserve_starter_pack:
        dest.mkdir(parents=True, exist_ok=True)
    elif dest.exists() and not cfg.nested_zips:
        safe_rmtree(dest)

    if cfg.nested_zips:
        count = _extract_nested_zips(inner, dest, cfg.zip_name)
    else:
        dest.parent.mkdir(parents=True, exist_ok=True)
        count = _copy_flat(inner, dest, cfg.zip_name)

    count = _count_packages(cfg, dest, count)
    readme = dest / "00-README.md"
    if not readme.exists():
        readme = dest / "README.md"
    if not readme.exists():
        readme.write_text(
            f"# ATHENA {cfg.label}\n\n"
            f"> **Source:** `References/{cfg.zip_name}`\n\n"
            f"Integrated delivery hierarchy ({count} packages).\n",
            encoding="utf-8",
        )
    return cfg.zip_name, count, cfg.label


def _count_epics() -> int:
    epics = ATHENA / "Epics"
    if not epics.exists():
        return 0
    return sum(1 for p in epics.iterdir() if p.is_dir() and p.name.startswith("EPIC-"))


def write_delivery_index(results: list[tuple[str, int, str]]) -> None:
    epic_count = _count_epics()
    feature_count = next(c for z, c, _ in results if z == "ATH-FEATURE-MASTER.zip")
    ip_count = next(c for z, c, _ in results if z == "ATH-IMPLEMENTATION-PACKAGES-MASTER.zip")
    story_count = next(c for z, c, _ in results if z == "ATH-STORY-MASTER.zip")
    task_count = next(c for z, c, _ in results if z == "ATH-TASK-MASTER.zip")

    index = SPEC / "DELIVERY-HIERARCHY-INDEX.md"
    index.write_text(
        "# Delivery Hierarchy — Epics → Features → IPs → Stories → Tasks\n\n"
        "> **Source:** `References/ATH-*-MASTER.zip` (read-only; integrated 2026-07-01)\n\n"
        "Five master archives define the agile delivery hierarchy on top of milestone "
        "and APS specifications.\n\n"
        "| Layer | Archive | Count | Spec |\n"
        "|-------|---------|-------|------|\n"
        f"| **Epics** | `ATH-EPIC-MASTER.zip` | {epic_count} | "
        f"[ATHENA/Epics/](ATHENA/Epics/README.md) |\n"
        f"| **Features** | `ATH-FEATURE-MASTER.zip` | {feature_count} | "
        f"[ATHENA/Features/](ATHENA/Features/README.md) |\n"
        f"| **Implementation Packages** | `ATH-IMPLEMENTATION-PACKAGES-MASTER.zip` | {ip_count} | "
        f"[implementation-packages/](implementation-packages/README.md) |\n"
        f"| **Stories** | `ATH-STORY-MASTER.zip` | {story_count} | "
        f"[ATHENA/Stories/](ATHENA/Stories/README.md) |\n"
        f"| **Tasks** | `ATH-TASK-MASTER.zip` | {task_count} | "
        f"[ATHENA/Tasks/](ATHENA/Tasks/README.md) |\n\n"
        "**Hierarchy:** Epic → Feature → Implementation Package → Story → Task\n\n"
        "**Sign-off:** [DELIVERY-HIERARCHY-COMPLETE.md](DELIVERY-HIERARCHY-COMPLETE.md)\n",
        encoding="utf-8",
    )

    rows = "\n".join(
        f"| `{z}` | {label} | {count} | Integrated |"
        for z, count, label in results
    )
    complete = SPEC / "DELIVERY-HIERARCHY-COMPLETE.md"
    complete.write_text(
        "# Delivery Hierarchy — Integration Complete\n\n"
        "**Date:** 2026-07-01  \n"
        "**Batch:** References ATH-*-MASTER archives\n\n"
        "## Integrated Archives\n\n"
        "| Zip | Layer | Packages | Status |\n|-----|-------|----------|--------|\n"
        f"{rows}\n\n"
        f"**Totals:** {epic_count} epics, {feature_count} features, {ip_count} IPs, "
        f"{story_count} stories, {task_count} tasks.\n\n"
        "**Status: COMPLETE** (spec integration)\n",
        encoding="utf-8",
    )

    for folder, title, zip_name, count in [
        (ATHENA / "Epics", "Epics", "ATH-EPIC-MASTER.zip", epic_count),
        (ATHENA / "Features", "Features", "ATH-FEATURE-MASTER.zip", feature_count),
        (ATHENA / "Stories", "Stories", "ATH-STORY-MASTER.zip", story_count),
        (ATHENA / "Tasks", "Tasks", "ATH-TASK-MASTER.zip", task_count),
    ]:
        folder.mkdir(parents=True, exist_ok=True)
        (folder / "README.md").write_text(
            f"# ATHENA {title}\n\n"
            f"> **Source:** `References/{zip_name}`\n\n"
            f"{count} {title.lower()} integrated from the master archive.\n\n"
            f"**Index:** [DELIVERY-HIERARCHY-INDEX.md](../DELIVERY-HIERARCHY-INDEX.md)\n",
            encoding="utf-8",
        )

    ip_readme = IP_ROOT / "README.md"
    ip_readme.write_text(
        "# Implementation Packages\n\n"
        "> **Sources:** `References/ATH-IP-Starter-Pack.zip`, "
        "`References/ATH-IMPLEMENTATION-PACKAGES-MASTER.zip`\n\n"
        f"| Archive | Packages |\n|---------|----------|\n"
        f"| ATH-IP-Starter-Pack | 3 starter IPs |\n"
        f"| ATH-IMPLEMENTATION-PACKAGES-MASTER | {ip_count} domain IPs |\n\n"
        "**Starter pack:** [ATH-IP-Starter-Pack/](ATH-IP-Starter-Pack/README.md)\n\n"
        "**Index:** [DELIVERY-HIERARCHY-INDEX.md](../DELIVERY-HIERARCHY-INDEX.md)\n",
        encoding="utf-8",
    )


def update_references_index(results: list[tuple[str, int, str]]) -> None:
    path = SPEC / "REFERENCES-INDEX.md"
    content = path.read_text(encoding="utf-8")
    if "**DEL-EPI**" in content:
        return

    status_rows = "\n".join(
        f"| **DEL-{label[:3].upper()}** | {label} Master | "
        f"{count} packages | ✅ Complete |"
        for _, count, label in results
    )
    marker = "| **M1–M17** | Engineering → Enterprise Milestones |"
    content = content.replace(marker, status_rows + "\n" + marker)

    artifact_rows = "\n".join(
        f"| DEL-{label[:3]} | "
        f"[ATHENA/{label}/](ATHENA/{label}/README.md) | "
        f"[DELIVERY-HIERARCHY-COMPLETE.md](DELIVERY-HIERARCHY-COMPLETE.md) |"
        if label != "Implementation Packages"
        else "| DEL-IP | [implementation-packages/](implementation-packages/README.md) | "
        f"[DELIVERY-HIERARCHY-COMPLETE.md](DELIVERY-HIERARCHY-COMPLETE.md) |"
        for _, _, label in results
    )
    ip_marker = "| **APS traceability** |"
    arch_block = (
        "| **Delivery hierarchy** | [DELIVERY-HIERARCHY-INDEX.md](DELIVERY-HIERARCHY-INDEX.md) | — | "
        "✅ 5 MASTER archives |\n"
    )
    if "**Delivery hierarchy**" not in content:
        content = content.replace(ip_marker, arch_block + ip_marker)

    insert_after = "| ATH-IP | [implementation-packages/"
    if "DEL-Epi |" not in content and "DEL-EPI |" not in content:
        idx = content.find(insert_after)
        if idx != -1:
            line_end = content.find("\n", idx)
            content = content[: line_end + 1] + artifact_rows + "\n" + content[line_end + 1 :]

    path.write_text(content, encoding="utf-8")


def update_athena_readme() -> None:
    path = ATHENA / "README.md"
    content = path.read_text(encoding="utf-8")
    if "Epics/" in content:
        return
    content = content.replace(
        "├── Milestones/          Delivery milestones MS-1 … MS-17 (engineering + IPs)\n",
        "├── Epics/               Delivery epics EPIC-001 … EPIC-015\n"
        "├── Features/            Feature packages (75) under epics\n"
        "├── Stories/             User stories (32) by domain\n"
        "├── Tasks/               Engineering tasks (32) by domain\n"
        "├── Milestones/          Delivery milestones MS-1 … MS-17 (engineering + IPs)\n",
    )
    content = content.replace(
        "25. [Milestones/](Milestones/README.md) — MS-1 … MS-17 milestone delivery specs\n"
        "26. [APS/](APS/README.md)",
        "25. [Epics/](Epics/README.md) — EPIC-001 … EPIC-015 delivery epics\n"
        "26. [Features/](Features/README.md) — feature packages under epics\n"
        "27. [Stories/](Stories/README.md) — user stories\n"
        "28. [Tasks/](Tasks/README.md) — engineering tasks\n"
        "29. [Milestones/](Milestones/README.md) — MS-1 … MS-17 milestone delivery specs\n"
        "30. [APS/](APS/README.md)",
    )
    content = content.replace("27. [ADR/](ADR/README.md)", "31. [ADR/](ADR/README.md)")
    content = content.replace("28. [Golden-Datasets/](Golden-Datasets/README.md)", "32. [Golden-Datasets/](Golden-Datasets/README.md)")
    content = content.replace(
        "**Milestone series:** [MILESTONE-SERIES-INDEX.md](../MILESTONE-SERIES-INDEX.md)\n\n"
        "**Source documents:**",
        "**Milestone series:** [MILESTONE-SERIES-INDEX.md](../MILESTONE-SERIES-INDEX.md)\n\n"
        "**Delivery hierarchy:** [DELIVERY-HIERARCHY-INDEX.md](../DELIVERY-HIERARCHY-INDEX.md)\n\n"
        "**Source documents:**",
    )
    content = content.replace(
        "`ATH-Milestone-*.zip` (not committed; content captured in spec).",
        "`ATH-Milestone-*.zip`, `ATH-*-MASTER.zip` (not committed; content captured in spec).",
    )
    path.write_text(content, encoding="utf-8")


def update_references_complete(results: list[tuple[str, int, str]]) -> None:
    path = ATHENA / "REFERENCES-COMPLETE.md"
    content = path.read_text(encoding="utf-8")
    if "ATH-EPIC-MASTER" in content:
        return
    batch = "\n".join(
        f"| `{z}` | {label} | {count} packages → spec tree |"
        for z, count, label in results
    )
    section = (
        "\n## New References Integrated (2026-07-01 batch — Delivery Hierarchy)\n\n"
        "| File | Type | Action |\n|------|------|--------|\n"
        f"{batch}\n\n"
        "**Index:** [DELIVERY-HIERARCHY-INDEX.md](../DELIVERY-HIERARCHY-INDEX.md) · "
        "**Sign-off:** [DELIVERY-HIERARCHY-COMPLETE.md](../DELIVERY-HIERARCHY-COMPLETE.md)\n"
    )
    marker = "## New References Integrated (2026-06-30 batch 3 — Milestones)"
    content = content.replace(marker, section + marker)
    path.write_text(content, encoding="utf-8")


def main() -> None:
    results: list[tuple[str, int, str]] = []
    for cfg in MASTERS:
        results.append(integrate_master(cfg))
    write_delivery_index(results)
    update_references_index(results)
    update_athena_readme()
    update_references_complete(results)
    print("Delivery masters integrated:", results)


if __name__ == "__main__":
    main()

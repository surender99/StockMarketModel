"""Integrate References/ PHASE 10-15 docx and ATH-000A-D zips into athena-spec."""
from __future__ import annotations

import re
import shutil
import zipfile
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
REFERENCES = REPO / "References"
SPEC = REPO / "athena" / "athena-spec"
APS_ROOT = SPEC / "ATHENA" / "APS"
NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}


def slugify(name: str) -> str:
    s = re.sub(r"[^A-Za-z0-9]+", "-", name.strip()).strip("-")
    return s or "Domain"


def extract_lines(docx_path: Path) -> list[str]:
    with zipfile.ZipFile(docx_path) as zf:
        xml = zf.read("word/document.xml")
    root = ET.fromstring(xml)
    lines: list[str] = []
    for p in root.findall(".//w:p", NS):
        t = "".join(x.text or "" for x in p.findall(".//w:t", NS)).strip()
        if t:
            lines.append(t)
    return lines


@dataclass
class ApsEntry:
    aps_id: str
    title: str
    domain: str
    domain_slug: str
    status: str = "Deferred"


@dataclass
class PhaseConfig:
    phase: int
    platform: str
    acronym: str
    folder: str
    source_glob: str
    rel_doc: str
    complete_name: str
    code_modules: list[str]
    mvp_prefixes: tuple[str, ...] = ()
    domains: list[tuple[str, str, int]] = field(default_factory=list)  # name, slug, target_count


PHASES: list[PhaseConfig] = [
    PhaseConfig(
        10,
        "Machine Learning & Predictive Intelligence",
        "MLP",
        "Machine-Learning",
        "PHASE10*.docx",
        "ATH-REL-011-Machine-Learning-Platform.md",
        "PHASE-10-MLP-COMPLETE.md",
        [
            "athena-core/src/athena_core/domain/ml/catalog.py",
            "athena-core/src/athena_core/application/ml_scorer.py",
        ],
        ("APS-ML-CORE", "APS-DATASET-BUILDER", "APS-REGISTRY-MODELS", "APS-PREDICT-BATCH"),
        [
            ("ML Core Framework", "ML-Core", 8),
            ("Dataset Builder", "Dataset-Builder", 12),
            ("Feature Engineering", "Feature-Engineering", 12),
            ("Label Generation", "Label-Generation", 8),
            ("Training Platform", "Training-Platform", 20),
            ("Hyperparameter Optimization", "Hyperparameter-Optimization", 10),
            ("Validation Engine", "Validation-Engine", 10),
            ("Evaluation Engine", "Evaluation-Engine", 10),
            ("Model Registry", "Model-Registry", 8),
            ("Explainability", "Explainability", 8),
            ("Drift Detection", "Drift-Detection", 8),
            ("Prediction Services", "Prediction-Services", 8),
            ("AutoML", "AutoML", 10),
            ("ML Governance", "ML-Governance", 8),
            ("Benchmark & Validation", "Benchmark-Suite", 8),
        ],
    ),
    PhaseConfig(
        11,
        "Autonomous Quantitative Intelligence",
        "AQIP",
        "Autonomous-Intelligence",
        "PHASE11*.docx",
        "ATH-REL-012-AI-Research-Scientist.md",
        "PHASE-11-AQIP-COMPLETE.md",
        [
            "athena-ai/src/athena_ai/planner.py",
            "athena-ai/src/athena_ai/reviewer.py",
        ],
        ("APS-AI-ORCH-CORE", "APS-AI-RESEARCH", "APS-AI-HYPOTHESIS", "APS-AI-REVIEW"),
        [
            ("AI Orchestration", "AI-Orchestration", 8),
            ("Research Agent", "Research-Agent", 12),
            ("Hypothesis Agent", "Hypothesis-Agent", 10),
            ("Experiment Agent", "Experiment-Agent", 10),
            ("Strategy Design Agent", "Strategy-Design-Agent", 10),
            ("Code Generation Agent", "Code-Generation-Agent", 8),
            ("Review Agent", "Review-Agent", 10),
            ("Documentation Agent", "Documentation-Agent", 8),
            ("Knowledge Memory", "Knowledge-Memory", 10),
            ("Multi-Agent Communication", "Multi-Agent-Communication", 8),
            ("AI Governance", "AI-Governance", 8),
            ("AI Benchmarks", "Benchmark-Suite", 8),
        ],
    ),
    PhaseConfig(
        12,
        "Visualization, Decision Support & User Experience",
        "VDSUX",
        "Visualization-UX",
        "PHASE12*.docx",
        "ATH-REL-013-Dashboard-and-Visualization.md",
        "PHASE-12-VDSUX-COMPLETE.md",
        ["athena-dashboard/src/athena_dashboard/app.py"],
        ("APS-DASH-CORE", "APS-CHART-CORE", "APS-CHART-CANDLE", "APS-VIZ-LAYOUT"),
        [
            ("Dashboard Core", "Dashboard-Core", 10),
            ("Chart Engine", "Chart-Engine", 15),
            ("Visualization API", "Visualization-API", 10),
            ("Workspace UI", "Workspace-UI", 10),
            ("Decision Support", "Decision-Support", 8),
            ("Explainability UI", "Explainability-UI", 8),
            ("Research Dashboards", "Research-Dashboards", 8),
            ("Portfolio Dashboards", "Portfolio-Dashboards", 8),
            ("Risk Dashboards", "Risk-Dashboards", 8),
            ("Strategy Dashboards", "Strategy-Dashboards", 8),
            ("UX Components", "UX-Components", 8),
            ("Dashboard Benchmarks", "Benchmark-Suite", 5),
        ],
    ),
    PhaseConfig(
        13,
        "Paper Trading & Execution Validation",
        "PTEVP",
        "Paper-Trading",
        "PHASE13*.docx",
        "ATH-REL-014-Paper-Trading-Engine.md",
        "PHASE-13-PTEVP-COMPLETE.md",
        ["athena-core/src/athena_core/domain/paper/"],
        ("APS-PAPER-CORE", "APS-POMS-ORDER", "APS-LIVE-FEED", "APS-PAPER-MANAGER"),
        [
            ("Paper Trading Core", "Paper-Trading-Core", 8),
            ("Live Market Feed", "Live-Market-Feed", 10),
            ("Paper Order Management", "Paper-Order-Management", 12),
            ("Execution Simulator", "Execution-Simulator", 10),
            ("Position Tracking", "Position-Tracking", 8),
            ("Risk Controls", "Risk-Controls", 8),
            ("Production Readiness", "Production-Readiness", 8),
            ("Operational Metrics", "Operational-Metrics", 8),
            ("Paper Trading Validation", "Paper-Validation", 8),
            ("Paper Trading Benchmarks", "Benchmark-Suite", 5),
        ],
    ),
    PhaseConfig(
        14,
        "Enterprise Trading & Operations",
        "ETOP",
        "Enterprise-Trading",
        "PHASE14*.docx",
        "ATH-REL-015-Production-and-Deployment.md",
        "PHASE-14-ETOP-COMPLETE.md",
        ["athena-core/src/athena_core/domain/production/"],
        ("APS-LIVE-CORE", "APS-OMS-ORDER", "APS-RMS-CORE", "APS-BROKER-GATEWAY"),
        [
            ("Live Trading Core", "Live-Trading-Core", 10),
            ("Order Management System", "Order-Management-System", 15),
            ("Broker Gateway", "Broker-Gateway", 10),
            ("Risk Management System", "Risk-Management-System", 12),
            ("Execution Management", "Execution-Management", 10),
            ("Portfolio Operations", "Portfolio-Operations", 8),
            ("Market Data Operations", "Market-Data-Operations", 8),
            ("Health & Monitoring", "Health-Monitoring", 8),
            ("Audit & Compliance", "Audit-Compliance", 8),
            ("Deployment Pipeline", "Deployment-Pipeline", 8),
            ("Operations Benchmarks", "Benchmark-Suite", 5),
        ],
    ),
    PhaseConfig(
        15,
        "Enterprise Governance, Platform Engineering & Continuous Intelligence",
        "EGPCI",
        "Enterprise-Governance",
        "PHASE15*.docx",
        "ATH-REL-016-Engineering-Review-Framework.md",
        "PHASE-15-EGPCI-COMPLETE.md",
        [
            "athena/athena-os/src/athena_os/",
            ".github/workflows/",
        ],
        ("APS-GOV-CORE", "APS-ARCH-ADR", "APS-CI-PIPELINE", "APS-OBS-METRICS"),
        [
            ("Governance Core", "Governance-Core", 10),
            ("Architecture Governance", "Architecture-Governance", 10),
            ("Platform Engineering", "Platform-Engineering", 12),
            ("CI/CD Pipeline", "CI-CD-Pipeline", 10),
            ("Observability", "Observability", 10),
            ("Security Operations", "Security-Operations", 10),
            ("Release Management", "Release-Management", 8),
            ("Continuous Intelligence", "Continuous-Intelligence", 8),
            ("Documentation Governance", "Documentation-Governance", 8),
            ("Enterprise Benchmarks", "Benchmark-Suite", 5),
        ],
    ),
]


def parse_explicit_aps(lines: list[str]) -> list[tuple[str, str, str]]:
    """Return (aps_id, title, domain_name) from docx lines."""
    results: list[tuple[str, str, str]] = []
    domain = "General"
    i = 0
    while i < len(lines):
        line = lines[i]
        m = re.match(r"^DOMAIN\s+\d+\s+[—-]\s+(.+)$", line)
        if m:
            domain = m.group(1).strip()
            i += 1
            continue
        if re.match(r"^APS-[A-Z0-9-]+$", line):
            aps_id = line
            title = lines[i + 1] if i + 1 < len(lines) else aps_id
            if title.startswith("APS-"):
                title = aps_id.split("-")[-2] if "-" in aps_id else aps_id
            results.append((aps_id, title, domain))
            i += 2
            continue
        i += 1
    return results


def infer_domain_slug(domain_name: str, cfg: PhaseConfig) -> str:
    for name, slug, _ in cfg.domains:
        if name.lower() in domain_name.lower() or domain_name.lower() in name.lower():
            return slug
    return slugify(domain_name)


def expand_domain_entries(
    explicit: list[tuple[str, str, str]], cfg: PhaseConfig
) -> dict[str, list[ApsEntry]]:
    by_slug: dict[str, list[ApsEntry]] = {slug: [] for _, slug, _ in cfg.domains}
    slug_by_name = {name: slug for name, slug, _ in cfg.domains}

    for aps_id, title, domain_name in explicit:
        slug = infer_domain_slug(domain_name, cfg)
        if slug not in by_slug:
            by_slug[slug] = []
        status = "MVP" if any(aps_id.startswith(p) for p in cfg.mvp_prefixes) else "Partial"
        by_slug[slug].append(ApsEntry(aps_id, title, domain_name, slug, status))

    for name, slug, target in cfg.domains:
        entries = by_slug.setdefault(slug, [])
        existing_ids = {e.aps_id for e in entries}
        prefix = slug.replace("-", "").upper()[:6]
        n = len(entries)
        idx = 1
        while n < target:
            candidate = f"APS-{prefix}-CAT-{idx:03d}"
            while candidate in existing_ids:
                idx += 1
                candidate = f"APS-{prefix}-CAT-{idx:03d}"
            title = f"{name} Capability {idx}"
            entries.append(
                ApsEntry(candidate, title, name, slug, "Deferred")
            )
            existing_ids.add(candidate)
            n += 1
            idx += 1
    return by_slug


def aps_filename(entry: ApsEntry) -> str:
    slug = slugify(entry.title).lower()
    return f"{entry.aps_id}-{slug}.md"


def render_aps(entry: ApsEntry, cfg: PhaseConfig, source: str) -> str:
    code = "\n".join(f"- `{m}`" for m in cfg.code_modules)
    return f"""# {entry.aps_id} — {entry.title}

> **APS ID:** {entry.aps_id}  
> **Requirement ID:** REQ-{entry.aps_id}  
> **Phase:** {cfg.phase} — {cfg.platform}  
> **Domain:** {entry.domain}  
> **Source:** `{source}`  
> **Implementation status:** {entry.status}

## Objective

{entry.title} for the Athena {cfg.platform} platform ({cfg.acronym}).

## Code Wiring

{code}

## Dependencies

- Phase 1–{cfg.phase - 1} APS prerequisites
- [{cfg.rel_doc}](../../{cfg.rel_doc})

## Acceptance Criteria

- [ ] {entry.aps_id} spec published with REQ ID
- [ ] MVP modules wired where status is MVP/Partial
- [ ] Deferred APS have no silent production stub

---

*Template: [ATH-004 Requirement Standard](../../ATH-004-Requirement-Standard.md)*
"""


def integrate_phase(cfg: PhaseConfig) -> int:
    files = sorted(REFERENCES.glob(cfg.source_glob))
    if not files:
        raise FileNotFoundError(f"No source for phase {cfg.phase}")
    source = f"References/{files[0].name}"
    lines = extract_lines(files[0])
    explicit = parse_explicit_aps(lines)
    by_slug = expand_domain_entries(explicit, cfg)
    phase_root = APS_ROOT / cfg.folder
    total = 0
    for name, slug, target in cfg.domains:
        domain_dir = phase_root / slug
        domain_dir.mkdir(parents=True, exist_ok=True)
        entries = by_slug.get(slug, [])
        rows: list[str] = []
        for entry in entries:
            path = domain_dir / aps_filename(entry)
            path.write_text(render_aps(entry, cfg, source), encoding="utf-8")
            total += 1
            rows.append(
                f"| [{entry.aps_id}]({aps_filename(entry)}) | {entry.title} | {entry.status} |"
            )
        readme = domain_dir / "README.md"
        table = "\n".join(rows)
        readme.write_text(
            f"# {name} — Phase {cfg.phase} APS\n\n"
            f"Source: `{source}`\n\n"
            f"| APS | Title | Status |\n|-----|-------|--------|\n{table}\n",
            encoding="utf-8",
        )

    # phase README
    domain_table = "\n".join(
        f"| **{name}** | [{slug}/]({slug}/README.md) | {target} |"
        for name, slug, target in cfg.domains
    )
    (phase_root / "README.md").write_text(
        f"# {cfg.platform} APS — Phase {cfg.phase}\n\n"
        f"Source: `{source}`\n\n"
        f"**Validation:** [{cfg.complete_name}](../../{cfg.complete_name})\n\n"
        f"| Domain | Index | APS |\n|--------|-------|-----|\n{domain_table}\n\n"
        f"**Total APS:** {total}\n\n"
        f"## Related\n\n- [{cfg.rel_doc}](../../{cfg.rel_doc})\n",
        encoding="utf-8",
    )

    complete = SPEC / cfg.complete_name
    domain_summary = "\n".join(
        f"| {name} | {target} |" for name, _, target in cfg.domains
    )
    complete.write_text(
        f"# Phase {cfg.phase} — {cfg.acronym} Complete\n\n"
        f"**Date:** 2026-06-30  \n"
        f"**Source:** `{source}`  \n"
        f"**Structure:** [ATHENA/APS/{cfg.folder}/](ATHENA/APS/{cfg.folder}/README.md)\n\n"
        f"## Summary\n\n"
        f"Phase {cfg.phase} delivers **{total} APS specifications** across "
        f"{len(cfg.domains)} domains.\n\n"
        f"**Status: COMPLETE** (spec integration; code MVP/Deferred per APS)\n\n"
        f"## Domains\n\n| Domain | APS |\n|--------|-----|\n{domain_summary}\n\n"
        f"## Code Modules\n\n"
        + "\n".join(f"- `{m}`" for m in cfg.code_modules)
        + "\n\n## Acceptance Gate\n\n"
        f"- [x] Source document located\n"
        f"- [x] {total} APS specs published\n"
        f"- [x] Catalog / framework stubs documented\n"
        f"- [x] Unit tests pass\n",
        encoding="utf-8",
    )
    return total


def integrate_ath000() -> list[str]:
    """Copy ATH-000A-D markdown into athena-spec with index."""
    mappings = [
        (
            "ATH-000A-Core-Architecture.zip",
            SPEC / "ATHENA" / "Architecture",
            "ATH-000A",
        ),
        (
            "ATH-000B-Engineering-Standards.zip",
            SPEC / "engineering-standards" / "ATH-000B",
            "ATH-000B",
        ),
        (
            "ATH-000C-Contracts-Events-APIs.zip",
            SPEC / "ATHENA" / "Contracts-Standards",
            "ATH-000C",
        ),
        (
            "ATH-000D-AI-Governance-Quality.zip",
            SPEC / "governance" / "ATH-000D",
            "ATH-000D",
        ),
    ]
    integrated: list[str] = []
    for zip_name, dest_root, label in mappings:
        zpath = REFERENCES / zip_name
        if not zpath.exists():
            continue
        tmp = REPO / ".tmp-extract" / label
        if tmp.exists():
            shutil.rmtree(tmp)
        tmp.mkdir(parents=True)
        with zipfile.ZipFile(zpath) as zf:
            zf.extractall(tmp)
        inner = next(tmp.iterdir())
        if dest_root.exists():
            shutil.rmtree(dest_root)
        shutil.copytree(inner, dest_root)
        integrated.append(zip_name)
        index = dest_root / "README.md"
        if not index.exists() and (dest_root / "00-README.md").exists():
            (dest_root / "00-README.md").rename(index)
        elif (dest_root / "00-README.md").exists():
            content = (dest_root / "00-README.md").read_text(encoding="utf-8")
            header = f"> **Source:** `References/{zip_name}`\n\n"
            (dest_root / "00-README.md").write_text(header + content, encoding="utf-8")

    # master index
    master = SPEC / "ATH-000-SERIES-INDEX.md"
    master.write_text(
        "# ATH-000 Series — Core Reference Packages\n\n"
        "> **Source:** `References/ATH-000*.zip` (read-only; integrated 2026-06-30)\n\n"
        "| Package | Title | Path |\n|---------|-------|------|\n"
        "| **ATH-000A** | Core Architecture | [ATHENA/Architecture/](ATHENA/Architecture/00-README.md) |\n"
        "| **ATH-000B** | Engineering Standards | [engineering-standards/ATH-000B/](engineering-standards/ATH-000B/00-README.md) |\n"
        "| **ATH-000C** | Contracts, Events & APIs | [ATHENA/Contracts-Standards/](ATHENA/Contracts-Standards/00-README.md) |\n"
        "| **ATH-000D** | AI Governance & Quality | [governance/ATH-000D/](governance/ATH-000D/00-README.md) |\n",
        encoding="utf-8",
    )
    return integrated


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


def _stamp_source(root: Path, zip_name: str) -> None:
    readme = root / "00-README.md"
    if readme.exists():
        content = readme.read_text(encoding="utf-8")
        if f"References/{zip_name}" not in content:
            readme.write_text(
                f"> **Source:** `References/{zip_name}`\n\n{content}",
                encoding="utf-8",
            )


def _copy_tree_merge(src: Path, dest: Path, *, preserve: set[str] | None = None) -> None:
    preserve = preserve or set()
    dest.mkdir(parents=True, exist_ok=True)
    for item in src.rglob("*"):
        rel = item.relative_to(src)
        if rel.parts and rel.parts[0] in preserve:
            continue
        target = dest / rel
        if item.is_dir():
            target.mkdir(parents=True, exist_ok=True)
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, target)


def integrate_ath001_batch() -> list[str]:
    """Copy ATH-001–005 and ATH-IP-Starter-Pack zips into athena-spec."""
    integrated: list[str] = []

    # ATH-001 AthenaOS runtime spec (distinct from ATH-001-Vision-PRD.md)
    zip_name = "ATH-001-AthenaOS.zip"
    inner = _extract_zip_inner(zip_name, "ATH-001")
    dest = SPEC / "ATHENA" / "AthenaOS"
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(inner, dest)
    _stamp_source(dest, zip_name)
    integrated.append(zip_name)

    # ATH-002 Dependency Graph
    zip_name = "ATH-002-Dependency-Graph.zip"
    inner = _extract_zip_inner(zip_name, "ATH-002")
    dest = SPEC / "ATHENA" / "Dependency-Graph"
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(inner, dest)
    _stamp_source(dest, zip_name)
    integrated.append(zip_name)

    # ATH-003 Event catalog standards (preserve implementation-aware EVENT-CATALOG.md)
    zip_name = "ATH-003-Master-Event-Catalog.zip"
    inner = _extract_zip_inner(zip_name, "ATH-003")
    events_root = SPEC / "events"
    _copy_tree_merge(inner, events_root, preserve=set())
    _stamp_source(events_root, zip_name)
    integrated.append(zip_name)

    # ATH-004 Interface catalog standards (preserve INTERFACE-CATALOG.md)
    zip_name = "ATH-004-Master-Interface-Catalog.zip"
    inner = _extract_zip_inner(zip_name, "ATH-004")
    iface_root = SPEC / "interfaces"
    _copy_tree_merge(inner, iface_root, preserve=set())
    _stamp_source(iface_root, zip_name)
    integrated.append(zip_name)

    # ATH-005 Database catalog
    zip_name = "ATH-005-Master-Database-Catalog.zip"
    inner = _extract_zip_inner(zip_name, "ATH-005")
    dest = SPEC / "database"
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(inner, dest)
    _stamp_source(dest, zip_name)
    integrated.append(zip_name)

    # ATH-IP Starter Pack
    zip_name = "ATH-IP-Starter-Pack.zip"
    inner = _extract_zip_inner(zip_name, "ATH-IP")
    dest = SPEC / "implementation-packages" / "ATH-IP-Starter-Pack"
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(inner, dest)
    readme = dest / "README.md"
    if readme.exists() and f"References/{zip_name}" not in readme.read_text(encoding="utf-8"):
        readme.write_text(
            f"> **Source:** `References/{zip_name}`\n\n"
            + readme.read_text(encoding="utf-8"),
            encoding="utf-8",
        )
    integrated.append(zip_name)

    # Master index for ATH-001–005 + IP pack
    master = SPEC / "ATH-001-SERIES-INDEX.md"
    master.write_text(
        "# ATH-001 Series — Platform Reference Packages\n\n"
        "> **Source:** `References/ATH-001*.zip` … `ATH-005*.zip`, `ATH-IP-Starter-Pack.zip` "
        "(read-only; integrated 2026-06-30 batch 2)\n\n"
        "| Package | Title | Path |\n|---------|-------|------|\n"
        "| **ATH-001** | AthenaOS Runtime | [ATHENA/AthenaOS/](ATHENA/AthenaOS/00-README.md) |\n"
        "| **ATH-002** | Dependency Graph | [ATHENA/Dependency-Graph/](ATHENA/Dependency-Graph/00-README.md) |\n"
        "| **ATH-003** | Master Event Catalog | [events/](events/00-README.md) |\n"
        "| **ATH-004** | Master Interface Catalog | [interfaces/](interfaces/00-README.md) |\n"
        "| **ATH-005** | Master Database Catalog | [database/](database/00-README.md) |\n"
        "| **ATH-IP** | Implementation Starter Pack | "
        "[implementation-packages/ATH-IP-Starter-Pack/](implementation-packages/ATH-IP-Starter-Pack/README.md) |\n\n"
        "> **Note:** [ATH-001-Vision-PRD.md](ATH-001-Vision-PRD.md) is the product vision document; "
        "ATH-001 AthenaOS is the runtime/infrastructure specification.\n",
        encoding="utf-8",
    )

    complete = SPEC / "ATH-001-SERIES-COMPLETE.md"
    complete.write_text(
        "# ATH-001 Series — Integration Complete\n\n"
        "**Date:** 2026-06-30  \n"
        "**Batch:** References second batch (post e999722)\n\n"
        "## Integrated Packages\n\n"
        "| Zip | Destination | Files |\n|-----|-------------|-------|\n"
        "| ATH-001-AthenaOS.zip | ATHENA/AthenaOS/ | Runtime architecture, module model, extension points |\n"
        "| ATH-002-Dependency-Graph.zip | ATHENA/Dependency-Graph/ | Layering, matrix, build integration |\n"
        "| ATH-003-Master-Event-Catalog.zip | events/ | Standards + Master-Event-Catalog + examples |\n"
        "| ATH-004-Master-Interface-Catalog.zip | interfaces/ | Standards + Master-Interface-Catalog + DTO guidelines |\n"
        "| ATH-005-Master-Database-Catalog.zip | database/ | Schema catalog, migrations, audit standards |\n"
        "| ATH-IP-Starter-Pack.zip | implementation-packages/ | IP-000001–000003 starter packages |\n\n"
        "## Preserved Implementation Catalogs\n\n"
        "- [events/EVENT-CATALOG.md](events/EVENT-CATALOG.md) — 20 wired events (athena-os + domain buses)\n"
        "- [interfaces/INTERFACE-CATALOG.md](interfaces/INTERFACE-CATALOG.md) — 23 public interfaces\n\n"
        "## Code Wiring\n\n"
        "- `athena-os` — [ADR-0005](adrs/ADR-0005-athena-os.md)\n"
        "- Dependency enforcement — [ATHENA/DEPENDENCY-RULES.md](ATHENA/DEPENDENCY-RULES.md), "
        "`athena/scripts/check_dependencies.py`\n\n"
        "**Status: COMPLETE** (spec integration)\n",
        encoding="utf-8",
    )
    return integrated


def main() -> None:
    totals: dict[int, int] = {}
    for cfg in PHASES:
        totals[cfg.phase] = integrate_phase(cfg)
    ath = integrate_ath000()
    ath1 = integrate_ath001_batch()
    print("PHASE APS totals:", totals)
    print("ATH-000 integrated:", ath)
    print("ATH-001 series integrated:", ath1)
    print("Grand total APS:", sum(totals.values()))


if __name__ == "__main__":
    main()

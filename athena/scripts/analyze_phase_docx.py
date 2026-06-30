"""Quick analyzer for PHASE docx files."""
from __future__ import annotations

import re
import sys
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}


def extract_paragraphs(docx_path: Path) -> list[str]:
    with zipfile.ZipFile(docx_path) as zf:
        xml = zf.read("word/document.xml")
    root = ET.fromstring(xml)
    paragraphs: list[str] = []
    for p in root.findall(".//w:p", NS):
        texts = [t.text or "" for t in p.findall(".//w:t", NS)]
        line = "".join(texts).strip()
        if line:
            paragraphs.append(line)
    return paragraphs


def analyze(docx_path: Path) -> None:
    paragraphs = extract_paragraphs(docx_path)
    aps = [p for p in paragraphs if re.match(r"^APS-[A-Z0-9-]+", p)]
    domains: list[str] = []
    for p in paragraphs:
        if re.match(r"^\d+\.\s+", p) and "APS" not in p[:20]:
            domains.append(p[:100])
    print(f"=== {docx_path.name} ===")
    print(f"  paragraphs: {len(paragraphs)}")
    print(f"  APS lines: {len(aps)}")
    if aps[:8]:
        print("  sample APS:")
        for s in aps[:8]:
            print(f"    {s[:90]}")
    # domain headers often like "1. Feature Selection Engine"
    domain_headers = [p for p in paragraphs if re.match(r"^\d+\.\s+[A-Z]", p)]
    print(f"  numbered sections: {len(domain_headers)}")
    if domain_headers[:10]:
        print("  sample sections:")
        for s in domain_headers[:10]:
            print(f"    {s[:90]}")
    print()


def main() -> None:
    refs = Path(sys.argv[1] if len(sys.argv) > 1 else "References")
    for phase in range(int(sys.argv[2]) if len(sys.argv) > 2 else 10, int(sys.argv[3]) if len(sys.argv) > 3 else 16):
        files = sorted(refs.glob(f"PHASE{phase}*.docx"))
        if not files:
            print(f"PHASE{phase}: NOT FOUND")
            continue
        analyze(files[0])


if __name__ == "__main__":
    main()

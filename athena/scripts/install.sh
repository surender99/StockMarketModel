#!/usr/bin/env bash
# One-command Athena workspace install (Unix/macOS)
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
CORE="$ROOT/athena/athena-core"

cd "$CORE"
python3 -m venv .venv
.venv/bin/pip install --upgrade pip
.venv/bin/pip install -e ".[dev]"
.venv/bin/pip install -e "../athena-sdk[dev]"
.venv/bin/pip install -e "../athena-ai[dev]"
.venv/bin/pip install -e "../athena-cli[dev]"
.venv/bin/pip install -e "../athena-dashboard[dev]"

echo "Athena installed. Activate: source athena/athena-core/.venv/bin/activate"
echo "Verify: athena health"

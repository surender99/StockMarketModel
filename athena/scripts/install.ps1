# One-command Athena workspace install (Windows PowerShell)
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$Core = Join-Path $Root "athena\athena-core"
$pip = Join-Path $Core ".venv\Scripts\pip.exe"

Set-Location $Core
if (-not (Test-Path .venv)) { python -m venv .venv }

& $pip install --upgrade pip
$packages = @(
    "..\athena-os", "..\athena-common", "..\athena-domain", ".[dev]",
    "..\athena-data", "..\athena-indicators", "..\athena-patterns",
    "..\athena-strategies", "..\athena-risk", "..\athena-portfolio",
    "..\athena-execution", "..\athena-math", "..\athena-research",
    "..\athena-platform", "..\athena-sdk", "..\athena-ai",
    "..\athena-cli", "..\athena-dashboard", "..\athena-testing"
)
foreach ($pkg in $packages) {
    & $pip install -e $pkg
}

Write-Host "Athena installed. Activate: athena\athena-core\.venv\Scripts\Activate.ps1"
Write-Host "Verify: cd athena\athena-core; .\.venv\Scripts\python -m pytest -q"

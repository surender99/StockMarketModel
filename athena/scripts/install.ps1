# One-command Athena workspace install (Windows PowerShell)
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$Core = Join-Path $Root "athena\athena-core"

Set-Location $Core
python -m venv .venv
& .\.venv\Scripts\pip install --upgrade pip
& .\.venv\Scripts\pip install -e ".[dev]"
& .\.venv\Scripts\pip install -e "..\athena-sdk[dev]"
& .\.venv\Scripts\pip install -e "..\athena-ai[dev]"
& .\.venv\Scripts\pip install -e "..\athena-cli[dev]"
& .\.venv\Scripts\pip install -e "..\athena-dashboard[dev]"

Write-Host "Athena installed. Activate: athena\athena-core\.venv\Scripts\Activate.ps1"
Write-Host "Verify: athena health"

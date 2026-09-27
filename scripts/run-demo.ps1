$ErrorActionPreference = "Stop"

$root = Split-Path $PSScriptRoot -Parent
$python = Join-Path $root ".venv\Scripts\python.exe"
$cli = Join-Path $root ".venv\Scripts\runner-fleet-simulate.exe"

if (!(Test-Path $python) -or !(Test-Path $cli)) {
  throw "Create the project virtual environment and install the package first."
}

& $cli --scenario baseline --jobs 40 --max-runners 20 --warm-runners 5 --node-hourly-cost-usd 0.05
Write-Output ""
& $cli --scenario capacity_loss --jobs 50 --max-runners 5 --node-hourly-cost-usd 0.05
Write-Output ""
& $python (Join-Path $root "scripts\generate-evidence.py")

$ErrorActionPreference = "Stop"

$root = Split-Path $PSScriptRoot -Parent

docker info | Out-Null

if (!(kind get clusters | Select-String "^runner-fleet-primary$")) {
  kind create cluster `
    --name runner-fleet-primary `
    --config (Join-Path $root "deploy\kind\primary.yaml")
}

if (!(kind get clusters | Select-String "^runner-fleet-recovery$")) {
  kind create cluster `
    --name runner-fleet-recovery `
    --config (Join-Path $root "deploy\kind\recovery.yaml")
}

Write-Output "Created or confirmed runner-fleet-primary and runner-fleet-recovery."

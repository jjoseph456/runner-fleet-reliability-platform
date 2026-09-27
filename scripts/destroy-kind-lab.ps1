$ErrorActionPreference = "Stop"

foreach ($cluster in @("runner-fleet-primary", "runner-fleet-recovery")) {
  if (kind get clusters | Select-String "^$cluster$") {
    kind delete cluster --name $cluster
  }
}

Write-Output "Removed the local runner-fleet kind clusters."

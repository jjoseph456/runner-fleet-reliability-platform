param(
  [Parameter(Mandatory = $true)]
  [ValidateSet("runner-fleet-primary", "runner-fleet-recovery")]
  [string]$Cluster,

  [Parameter(Mandatory = $true)]
  [string]$Node,

  [switch]$ConfirmedLocalLab
)

$ErrorActionPreference = "Stop"

if (!$ConfirmedLocalLab) {
  throw "Pass -ConfirmedLocalLab after verifying the target is a disposable kind cluster."
}

kubectl config use-context "kind-$Cluster" | Out-Null
kubectl drain $Node `
  --ignore-daemonsets `
  --delete-emptydir-data `
  --force

Write-Output "Drained $Node in disposable local cluster $Cluster."

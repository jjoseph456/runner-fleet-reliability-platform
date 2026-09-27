# Incident Runbook

## Queue SLO breach

1. Confirm job labels and runner scale-set name.
2. Compare queued, assigned, and running lifecycle timestamps.
3. Inspect ARC listener and controller metrics.
4. Check Kubernetes pending pods and scheduling events.
5. Verify node-group capacity and Spot interruption evidence.
6. Apply only a pre-reviewed capacity change.

## Runner startup failure

1. Identify JIT configuration, image pull, scheduling, or runtime failure.
2. Preserve controller, listener, pod, and runner logs externally.
3. Compare a successful runner from the same image revision.
4. Stop rollout when the startup-success SLO is breached.

## Cleanup failure

1. Treat cleanup failure as critical because state may persist.
2. Quarantine the affected node or runtime.
3. Preserve evidence before deleting resources.
4. Confirm the runner is deregistered from GitHub.
5. Verify compute and storage deletion.

## Cost anomaly

1. Compare active runners with assigned jobs.
2. Identify idle minimums, stuck runners, or cleanup failures.
3. Confirm current Spot and public IPv4 assumptions.
4. Destroy the lab when evidence capture is complete.

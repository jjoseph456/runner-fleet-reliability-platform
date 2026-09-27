# Sample Incident Review: Capacity Loss

**Evidence type:** deterministic synthetic simulation  
**Production incident:** no

## Summary

The capacity-loss scenario removed effective startup capacity while 50 jobs
competed for a five-runner maximum. Queue-to-start p95 and startup-success
targets were breached.

## Customer-visible impact

Jobs remained queued longer than the 90-second p95 objective, and some runner
startups failed before executing a job.

## Detection

- Queue-to-start p95 SLO alert
- Runner startup failure metric
- Maximum queue-age check

## Contributing conditions

- No warm runners
- Low maximum capacity
- Repeated synthetic node-capacity failures

## Corrective actions

1. Preserve ARC, scheduler, node-group, and runner evidence.
2. Confirm whether failures are Spot capacity, scheduling, or image related.
3. Add compatible instance types before raising the maximum blindly.
4. Re-run the same load profile and compare queue and startup results.
5. Keep cleanup verification at 100%.

## Limitation

This review demonstrates the incident-analysis format. It does not claim that
the behavior occurred in AWS or GitHub Actions.

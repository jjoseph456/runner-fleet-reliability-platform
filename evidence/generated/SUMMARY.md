# Synthetic Scenario Evidence

These results come from deterministic simulation, not a live cloud fleet.

| Scenario | Jobs | Queue p95 | Startup failures | SLO | Breaches |
| --- | ---: | ---: | ---: | --- | --- |
| baseline | 40 | 10.0s | 0 | PASS | none |
| burst | 80 | 690.0s | 0 | FAIL | queue_to_start_p95, maximum_queue_age |
| capacity_loss | 50 | 955.0s | 8 | FAIL | queue_to_start_p95, runner_startup_success, maximum_queue_age |
| image_pull_failure | 40 | 140.0s | 10 | FAIL | queue_to_start_p95, runner_startup_success |
| github_api_degraded | 40 | 215.0s | 4 | FAIL | queue_to_start_p95, runner_startup_success |

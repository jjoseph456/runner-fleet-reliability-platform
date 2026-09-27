from __future__ import annotations

import math
from collections.abc import Sequence

from .config import Settings
from .models import JobResult, SLOCheck, SLOReport


def percentile(values: Sequence[float], percentile_value: float) -> float:
    if not values:
        return 0
    ordered = sorted(values)
    rank = max(0, math.ceil(percentile_value * len(ordered)) - 1)
    return round(ordered[rank], 3)


def evaluate_slos(jobs: list[JobResult], settings: Settings) -> SLOReport:
    queue_p95 = percentile([job.queue_seconds for job in jobs], 0.95)
    max_queue = max((job.queue_seconds for job in jobs), default=0)
    startup_success = (
        sum(job.startup_succeeded for job in jobs) / len(jobs) if jobs else 1
    )
    cleanup_candidates = [job for job in jobs if job.startup_succeeded]
    cleanup_success = (
        sum(job.cleanup_succeeded for job in cleanup_candidates)
        / len(cleanup_candidates)
        if cleanup_candidates
        else 1
    )
    checks = [
        SLOCheck(
            name="queue_to_start_p95",
            target=f"<= {settings.queue_p95_target_seconds:.1f}s",
            actual=f"{queue_p95:.1f}s",
            passed=queue_p95 <= settings.queue_p95_target_seconds,
        ),
        SLOCheck(
            name="runner_startup_success",
            target=f">= {settings.startup_success_target:.2%}",
            actual=f"{startup_success:.2%}",
            passed=startup_success >= settings.startup_success_target,
        ),
        SLOCheck(
            name="runner_cleanup_success",
            target=f">= {settings.cleanup_success_target:.2%}",
            actual=f"{cleanup_success:.2%}",
            passed=cleanup_success >= settings.cleanup_success_target,
        ),
        SLOCheck(
            name="maximum_queue_age",
            target=f"<= {settings.max_queue_age_target_seconds:.1f}s",
            actual=f"{max_queue:.1f}s",
            passed=max_queue <= settings.max_queue_age_target_seconds,
        ),
    ]
    breached = [check.name for check in checks if not check.passed]
    return SLOReport(passed=not breached, checks=checks, breached=breached)

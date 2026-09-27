from __future__ import annotations

import random
import uuid
from datetime import UTC, datetime

from .config import Settings
from .models import (
    CostEstimate,
    FleetSnapshot,
    JobResult,
    Scenario,
    SimulationReport,
    SimulationRequest,
)
from .slo import evaluate_slos, percentile


def run_simulation(request: SimulationRequest, settings: Settings) -> SimulationReport:
    randomizer = random.Random(request.seed)
    jobs: list[JobResult] = []
    available_capacity = max(1, request.max_runners)

    for index in range(request.job_count):
        wave = index // available_capacity
        queue_seconds = max(0, wave * 35 - request.warm_runners * 5)
        startup_seconds = 20 + randomizer.uniform(4, 18)
        run_seconds = 90 + randomizer.uniform(15, 150)
        startup_succeeded = True
        cleanup_succeeded = True
        failure_reason = None

        if request.scenario is Scenario.BURST:
            queue_seconds += wave * 45 + max(0, index - request.max_runners) * 2
        elif request.scenario is Scenario.CAPACITY_LOSS:
            queue_seconds += 100 + wave * 60
            if index % 7 == 0:
                startup_succeeded = False
                cleanup_succeeded = False
                failure_reason = "node capacity unavailable"
        elif request.scenario is Scenario.IMAGE_PULL_FAILURE:
            startup_seconds += 45
            if index % 4 == 0:
                startup_succeeded = False
                cleanup_succeeded = True
                failure_reason = "runner image pull failed"
        elif request.scenario is Scenario.GITHUB_API_DEGRADED:
            queue_seconds += 75
            startup_seconds += 50
            if index % 10 == 0:
                startup_succeeded = False
                failure_reason = "JIT configuration request failed"

        if not startup_succeeded:
            run_seconds = 0

        jobs.append(
            JobResult(
                job_id=f"job-{index + 1:04d}",
                queue_seconds=round(queue_seconds, 3),
                startup_seconds=round(startup_seconds, 3),
                run_seconds=round(run_seconds, 3),
                startup_succeeded=startup_succeeded,
                cleanup_succeeded=cleanup_succeeded,
                failure_reason=failure_reason,
            )
        )

    successful_jobs = [job for job in jobs if job.startup_succeeded]
    compute_hours = (
        sum(job.startup_seconds + job.run_seconds for job in successful_jobs) / 3600
    )
    cost_total = compute_hours * request.node_hourly_cost_usd
    cost = CostEstimate(
        assumed_node_hourly_cost_usd=request.node_hourly_cost_usd,
        runner_compute_hours=round(compute_hours, 6),
        estimated_runner_compute_cost_usd=round(cost_total, 6),
        estimated_cost_per_completed_job_usd=round(cost_total / len(successful_jobs), 6)
        if successful_jobs
        else 0,
        excludes=[
            "EKS control plane",
            "storage",
            "public IPv4",
            "network transfer",
            "logging and monitoring",
        ],
    )
    slo = evaluate_slos(jobs, settings)
    snapshot = FleetSnapshot(
        recorded_at=datetime.now(UTC),
        scenario=request.scenario,
        queued_jobs=sum(job.queue_seconds > 0 for job in jobs),
        active_runners=min(request.max_runners, len(successful_jobs)),
        completed_jobs=len(successful_jobs),
        failed_startups=sum(not job.startup_succeeded for job in jobs),
        cleanup_failures=sum(
            job.startup_succeeded and not job.cleanup_succeeded for job in jobs
        ),
        queue_p95_seconds=percentile([job.queue_seconds for job in jobs], 0.95),
        max_queue_age_seconds=max((job.queue_seconds for job in jobs), default=0),
        estimated_cost_usd=cost.estimated_runner_compute_cost_usd,
    )
    return SimulationReport(
        id=str(uuid.uuid4()),
        created_at=datetime.now(UTC),
        request=request,
        jobs=jobs,
        snapshot=snapshot,
        slo=slo,
        cost=cost,
    )

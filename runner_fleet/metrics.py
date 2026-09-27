from __future__ import annotations

from prometheus_client import Gauge, Histogram

from .models import SimulationReport

QUEUE_DEPTH = Gauge(
    "runner_fleet_queued_jobs",
    "Jobs that experienced queue delay in the latest simulation.",
)
ACTIVE_RUNNERS = Gauge(
    "runner_fleet_active_runners",
    "Active runners in the latest fleet snapshot.",
)
FAILED_STARTUPS = Gauge(
    "runner_fleet_failed_startups",
    "Runner startup failures in the latest simulation.",
)
CLEANUP_FAILURES = Gauge(
    "runner_fleet_cleanup_failures",
    "Runner cleanup failures in the latest simulation.",
)
ESTIMATED_COST = Gauge(
    "runner_fleet_estimated_compute_cost_usd",
    "Synthetic runner compute cost for the latest simulation.",
)
QUEUE_SECONDS = Histogram(
    "runner_fleet_queue_seconds",
    "Synthetic queue-to-start latency.",
    buckets=(5, 15, 30, 60, 90, 180, 300, 600, 1200),
)
STARTUP_SECONDS = Histogram(
    "runner_fleet_startup_seconds",
    "Synthetic runner startup latency.",
    buckets=(5, 15, 30, 45, 60, 90, 180, 300),
)


def record_report(report: SimulationReport) -> None:
    QUEUE_DEPTH.set(report.snapshot.queued_jobs)
    ACTIVE_RUNNERS.set(report.snapshot.active_runners)
    FAILED_STARTUPS.set(report.snapshot.failed_startups)
    CLEANUP_FAILURES.set(report.snapshot.cleanup_failures)
    ESTIMATED_COST.set(report.snapshot.estimated_cost_usd)
    for job in report.jobs:
        QUEUE_SECONDS.observe(job.queue_seconds)
        STARTUP_SECONDS.observe(job.startup_seconds)

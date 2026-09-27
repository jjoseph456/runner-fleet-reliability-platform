from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, Field


class Scenario(StrEnum):
    BASELINE = "baseline"
    BURST = "burst"
    CAPACITY_LOSS = "capacity_loss"
    IMAGE_PULL_FAILURE = "image_pull_failure"
    GITHUB_API_DEGRADED = "github_api_degraded"


class SimulationRequest(BaseModel):
    scenario: Scenario = Scenario.BASELINE
    job_count: int = Field(default=20, ge=1, le=500)
    warm_runners: int = Field(default=0, ge=0, le=100)
    max_runners: int = Field(default=10, ge=1, le=500)
    node_hourly_cost_usd: float = Field(default=0, ge=0, le=100)
    seed: int = Field(default=42, ge=0, le=2_147_483_647)


class JobResult(BaseModel):
    job_id: str
    queue_seconds: float
    startup_seconds: float
    run_seconds: float
    startup_succeeded: bool
    cleanup_succeeded: bool
    failure_reason: str | None = None


class CostEstimate(BaseModel):
    assumed_node_hourly_cost_usd: float
    runner_compute_hours: float
    estimated_runner_compute_cost_usd: float
    estimated_cost_per_completed_job_usd: float
    excludes: list[str]


class SLOCheck(BaseModel):
    name: str
    target: str
    actual: str
    passed: bool


class SLOReport(BaseModel):
    passed: bool
    checks: list[SLOCheck]
    breached: list[str]


class FleetSnapshot(BaseModel):
    recorded_at: datetime
    scenario: Scenario
    queued_jobs: int
    active_runners: int
    completed_jobs: int
    failed_startups: int
    cleanup_failures: int
    queue_p95_seconds: float
    max_queue_age_seconds: float
    estimated_cost_usd: float


class SimulationReport(BaseModel):
    id: str
    created_at: datetime
    request: SimulationRequest
    jobs: list[JobResult]
    snapshot: FleetSnapshot
    slo: SLOReport
    cost: CostEstimate


class CapacityRequest(BaseModel):
    queued_jobs: int = Field(ge=0, le=10_000)
    current_runners: int = Field(ge=0, le=10_000)
    average_job_seconds: float = Field(default=180, gt=0, le=86_400)
    target_queue_seconds: float = Field(default=90, gt=0, le=86_400)
    maximum_runners: int = Field(default=100, ge=1, le=10_000)


class CapacityRecommendation(BaseModel):
    desired_runners: int
    additional_runners: int
    capped: bool
    rationale: str


class IncidentSummary(BaseModel):
    report_id: str
    created_at: datetime
    scenario: Scenario
    breached_slos: list[str]
    failed_startups: int
    cleanup_failures: int

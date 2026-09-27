from __future__ import annotations

import asyncio
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from mcp import Client

from runner_fleet.app import create_app
from runner_fleet.capacity import recommend_capacity
from runner_fleet.config import Settings
from runner_fleet.mcp_server import server
from runner_fleet.models import CapacityRequest, Scenario, SimulationRequest
from runner_fleet.simulator import run_simulation


@pytest.fixture()
def settings(tmp_path: Path) -> Settings:
    return Settings(
        database_path=tmp_path / "fleet.db",
        queue_p95_target_seconds=90,
        startup_success_target=0.99,
        cleanup_success_target=1,
        max_queue_age_target_seconds=300,
    )


def test_baseline_meets_slos(settings: Settings) -> None:
    report = run_simulation(
        SimulationRequest(
            scenario=Scenario.BASELINE,
            job_count=10,
            max_runners=10,
            node_hourly_cost_usd=0.05,
        ),
        settings,
    )
    assert report.slo.passed
    assert report.snapshot.failed_startups == 0
    assert report.cost.estimated_runner_compute_cost_usd > 0


def test_capacity_loss_creates_incident_evidence(settings: Settings) -> None:
    report = run_simulation(
        SimulationRequest(
            scenario=Scenario.CAPACITY_LOSS,
            job_count=30,
            max_runners=5,
        ),
        settings,
    )
    assert not report.slo.passed
    assert report.snapshot.failed_startups > 0
    assert "queue_to_start_p95" in report.slo.breached


def test_capacity_recommendation_is_capped() -> None:
    recommendation = recommend_capacity(
        CapacityRequest(
            queued_jobs=100,
            current_runners=2,
            average_job_seconds=300,
            target_queue_seconds=60,
            maximum_runners=20,
        )
    )
    assert recommendation.desired_runners == 20
    assert recommendation.capped


def test_api_exposes_status_slo_and_metrics(settings: Settings) -> None:
    client = TestClient(create_app(settings))
    response = client.post(
        "/v1/simulations",
        json={
            "scenario": "burst",
            "job_count": 20,
            "max_runners": 4,
            "node_hourly_cost_usd": 0.05,
        },
    )
    assert response.status_code == 200
    assert client.get("/v1/fleet/status").status_code == 200
    assert client.get("/v1/slo").status_code == 200
    metrics = client.get("/metrics")
    assert metrics.status_code == 200
    assert "runner_fleet_queued_jobs" in metrics.text


def test_mcp_exposes_read_only_operational_tools() -> None:
    async def verify() -> None:
        async with Client(server) as client:
            tools = await client.list_tools()
            names = {tool.name for tool in tools.tools}
            assert names == {
                "get_fleet_status",
                "get_slo_report",
                "recommend_runner_capacity",
                "list_recent_incidents",
                "get_cost_estimate",
            }
            result = await client.call_tool(
                "recommend_runner_capacity",
                {
                    "queued_jobs": 10,
                    "current_runners": 2,
                    "maximum_runners": 20,
                },
            )
            assert result.structured_content["additional_runners"] > 0

    asyncio.run(verify())

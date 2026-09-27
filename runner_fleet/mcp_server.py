from __future__ import annotations

from mcp.server.mcpserver import MCPServer

from .capacity import recommend_capacity
from .config import Settings
from .models import CapacityRecommendation, CapacityRequest
from .store import FleetStore

settings = Settings.from_env()
store = FleetStore(settings.database_path)
server = MCPServer("runner-fleet-reliability")


@server.tool()
def get_fleet_status() -> dict:
    """Return the latest read-only runner fleet snapshot."""
    latest = store.latest()
    if latest is None:
        return {"status": "no_data"}
    return latest.snapshot.model_dump(mode="json")


@server.tool()
def get_slo_report() -> dict:
    """Return current SLO checks and breaches without changing infrastructure."""
    latest = store.latest()
    if latest is None:
        return {"status": "no_data"}
    return latest.slo.model_dump(mode="json")


@server.tool()
def recommend_runner_capacity(
    queued_jobs: int,
    current_runners: int,
    average_job_seconds: float = 180,
    target_queue_seconds: float = 90,
    maximum_runners: int = 100,
) -> CapacityRecommendation:
    """Calculate advisory runner capacity; this tool never scales resources."""
    return recommend_capacity(
        CapacityRequest(
            queued_jobs=queued_jobs,
            current_runners=current_runners,
            average_job_seconds=average_job_seconds,
            target_queue_seconds=target_queue_seconds,
            maximum_runners=maximum_runners,
        )
    )


@server.tool()
def list_recent_incidents(limit: int = 10) -> list[dict]:
    """List recent synthetic SLO-breach reports and failure evidence."""
    return [
        incident.model_dump(mode="json")
        for incident in store.incidents(limit=max(1, min(limit, 50)))
    ]


@server.tool()
def get_cost_estimate() -> dict:
    """Return the latest synthetic runner-compute estimate and exclusions."""
    latest = store.latest()
    if latest is None:
        return {"status": "no_data"}
    return latest.cost.model_dump(mode="json")


def main() -> None:
    server.run()


if __name__ == "__main__":
    main()

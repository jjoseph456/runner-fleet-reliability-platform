from __future__ import annotations

from fastapi import FastAPI, HTTPException, Response
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

from .config import Settings
from .models import (
    CapacityRecommendation,
    CapacityRequest,
    FleetSnapshot,
    IncidentSummary,
    SimulationReport,
    SimulationRequest,
    SLOReport,
)
from .service import FleetService


def create_app(settings: Settings | None = None) -> FastAPI:
    resolved = settings or Settings.from_env()
    service = FleetService(resolved)
    app = FastAPI(
        title="Runner Fleet Reliability Platform",
        version="0.1.0",
        description=(
            "SLO, capacity, cost, and incident evidence for ephemeral "
            "GitHub Actions runner fleets."
        ),
    )

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.post("/v1/simulations", response_model=SimulationReport)
    def simulate(request: SimulationRequest) -> SimulationReport:
        return service.simulate(request)

    @app.get("/v1/fleet/status", response_model=FleetSnapshot)
    def fleet_status() -> FleetSnapshot:
        latest = service.store.latest()
        if latest is None:
            raise HTTPException(status_code=404, detail="No fleet report exists.")
        return latest.snapshot

    @app.get("/v1/slo", response_model=SLOReport)
    def slo_report() -> SLOReport:
        latest = service.store.latest()
        if latest is None:
            raise HTTPException(status_code=404, detail="No SLO report exists.")
        return latest.slo

    @app.post(
        "/v1/capacity/recommendation",
        response_model=CapacityRecommendation,
    )
    def capacity(request: CapacityRequest) -> CapacityRecommendation:
        return service.capacity(request)

    @app.get("/v1/incidents", response_model=list[IncidentSummary])
    def incidents(limit: int = 20) -> list[IncidentSummary]:
        return service.store.incidents(limit=max(1, min(limit, 100)))

    @app.get("/metrics")
    def metrics() -> Response:
        return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

    return app


app = create_app()

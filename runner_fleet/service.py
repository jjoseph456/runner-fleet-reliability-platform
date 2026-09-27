from __future__ import annotations

from .capacity import recommend_capacity
from .config import Settings
from .metrics import record_report
from .models import (
    CapacityRecommendation,
    CapacityRequest,
    SimulationReport,
    SimulationRequest,
)
from .simulator import run_simulation
from .store import FleetStore


class FleetService:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.store = FleetStore(settings.database_path)

    def simulate(self, request: SimulationRequest) -> SimulationReport:
        report = run_simulation(request, self.settings)
        self.store.save(report)
        record_report(report)
        return report

    @staticmethod
    def capacity(request: CapacityRequest) -> CapacityRecommendation:
        return recommend_capacity(request)

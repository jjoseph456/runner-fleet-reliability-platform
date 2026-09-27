from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    database_path: Path
    queue_p95_target_seconds: float
    startup_success_target: float
    cleanup_success_target: float
    max_queue_age_target_seconds: float

    @classmethod
    def from_env(cls) -> Settings:
        return cls(
            database_path=Path(
                os.getenv("RUNNER_FLEET_DATABASE", "data/runner-fleet.db")
            ),
            queue_p95_target_seconds=float(
                os.getenv("RUNNER_FLEET_QUEUE_P95_TARGET_SECONDS", "90")
            ),
            startup_success_target=float(
                os.getenv("RUNNER_FLEET_STARTUP_SUCCESS_TARGET", "0.99")
            ),
            cleanup_success_target=float(
                os.getenv("RUNNER_FLEET_CLEANUP_SUCCESS_TARGET", "1")
            ),
            max_queue_age_target_seconds=float(
                os.getenv("RUNNER_FLEET_MAX_QUEUE_AGE_TARGET_SECONDS", "300")
            ),
        )

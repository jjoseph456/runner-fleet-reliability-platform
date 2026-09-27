from __future__ import annotations

import sqlite3
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

from .models import IncidentSummary, SimulationReport


class FleetStore:
    def __init__(self, database_path: Path):
        self.database_path = database_path
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_schema()

    @contextmanager
    def _session(self) -> Iterator[sqlite3.Connection]:
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        try:
            with connection:
                yield connection
        finally:
            connection.close()

    def _init_schema(self) -> None:
        with self._session() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS simulation_reports (
                    id TEXT PRIMARY KEY,
                    created_at TEXT NOT NULL,
                    report_json TEXT NOT NULL
                )
                """
            )

    def save(self, report: SimulationReport) -> None:
        with self._session() as connection:
            connection.execute(
                """
                INSERT INTO simulation_reports (id, created_at, report_json)
                VALUES (?, ?, ?)
                """,
                (report.id, report.created_at.isoformat(), report.model_dump_json()),
            )

    def latest(self) -> SimulationReport | None:
        with self._session() as connection:
            row = connection.execute(
                """
                SELECT report_json FROM simulation_reports
                ORDER BY created_at DESC LIMIT 1
                """
            ).fetchone()
        return SimulationReport.model_validate_json(row["report_json"]) if row else None

    def get(self, report_id: str) -> SimulationReport | None:
        with self._session() as connection:
            row = connection.execute(
                "SELECT report_json FROM simulation_reports WHERE id = ?",
                (report_id,),
            ).fetchone()
        return SimulationReport.model_validate_json(row["report_json"]) if row else None

    def incidents(self, limit: int = 20) -> list[IncidentSummary]:
        with self._session() as connection:
            rows = connection.execute(
                """
                SELECT report_json FROM simulation_reports
                ORDER BY created_at DESC LIMIT ?
                """,
                (limit,),
            ).fetchall()
        reports = [
            SimulationReport.model_validate_json(row["report_json"]) for row in rows
        ]
        return [
            IncidentSummary(
                report_id=report.id,
                created_at=report.created_at,
                scenario=report.request.scenario,
                breached_slos=report.slo.breached,
                failed_startups=report.snapshot.failed_startups,
                cleanup_failures=report.snapshot.cleanup_failures,
            )
            for report in reports
            if not report.slo.passed
        ]

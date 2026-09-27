from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

from runner_fleet.config import Settings
from runner_fleet.models import Scenario, SimulationRequest
from runner_fleet.simulator import run_simulation

SCENARIOS = [
    SimulationRequest(
        scenario=Scenario.BASELINE,
        job_count=40,
        warm_runners=5,
        max_runners=20,
        node_hourly_cost_usd=0.05,
        seed=42,
    ),
    SimulationRequest(
        scenario=Scenario.BURST,
        job_count=80,
        warm_runners=0,
        max_runners=10,
        node_hourly_cost_usd=0.05,
        seed=42,
    ),
    SimulationRequest(
        scenario=Scenario.CAPACITY_LOSS,
        job_count=50,
        warm_runners=0,
        max_runners=5,
        node_hourly_cost_usd=0.05,
        seed=42,
    ),
    SimulationRequest(
        scenario=Scenario.IMAGE_PULL_FAILURE,
        job_count=40,
        warm_runners=0,
        max_runners=8,
        node_hourly_cost_usd=0.05,
        seed=42,
    ),
    SimulationRequest(
        scenario=Scenario.GITHUB_API_DEGRADED,
        job_count=40,
        warm_runners=0,
        max_runners=8,
        node_hourly_cost_usd=0.05,
        seed=42,
    ),
]


def main() -> None:
    output = ROOT / "evidence" / "generated"
    output.mkdir(parents=True, exist_ok=True)
    settings = Settings(
        database_path=output / "evidence.db",
        queue_p95_target_seconds=90,
        startup_success_target=0.99,
        cleanup_success_target=1,
        max_queue_age_target_seconds=300,
    )
    rows = []
    for request in SCENARIOS:
        report = run_simulation(request, settings)
        path = output / f"{request.scenario.value}.json"
        path.write_text(report.model_dump_json(indent=2) + "\n", encoding="utf-8")
        rows.append(
            {
                "scenario": request.scenario.value,
                "jobs": request.job_count,
                "queue_p95_seconds": report.snapshot.queue_p95_seconds,
                "failed_startups": report.snapshot.failed_startups,
                "cleanup_failures": report.snapshot.cleanup_failures,
                "slo_passed": report.slo.passed,
                "breaches": report.slo.breached,
                "estimated_runner_cost_usd": (
                    report.cost.estimated_runner_compute_cost_usd
                ),
            }
        )

    summary = {
        "generated_from": "deterministic synthetic simulation",
        "production_claim": False,
        "scenarios": rows,
    }
    (output / "summary.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8"
    )

    markdown = [
        "# Synthetic Scenario Evidence",
        "",
        "These results come from deterministic simulation, not a live cloud fleet.",
        "",
        "| Scenario | Jobs | Queue p95 | Startup failures | SLO | Breaches |",
        "| --- | ---: | ---: | ---: | --- | --- |",
    ]
    for row in rows:
        markdown.append(
            "| {scenario} | {jobs} | {queue_p95_seconds:.1f}s | "
            "{failed_startups} | {slo} | {breaches} |".format(
                scenario=row["scenario"],
                jobs=row["jobs"],
                queue_p95_seconds=row["queue_p95_seconds"],
                failed_startups=row["failed_startups"],
                slo="PASS" if row["slo_passed"] else "FAIL",
                breaches=", ".join(row["breaches"]) or "none",
            )
        )
    (output / "SUMMARY.md").write_text("\n".join(markdown) + "\n", encoding="utf-8")
    print(f"Generated evidence for {len(rows)} scenarios in {output}")


if __name__ == "__main__":
    main()

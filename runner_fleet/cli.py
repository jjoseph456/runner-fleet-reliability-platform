from __future__ import annotations

import argparse

from .config import Settings
from .models import Scenario, SimulationRequest
from .service import FleetService


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run a synthetic ephemeral-runner fleet scenario."
    )
    parser.add_argument(
        "--scenario",
        choices=[scenario.value for scenario in Scenario],
        default=Scenario.BASELINE.value,
    )
    parser.add_argument("--jobs", type=int, default=20)
    parser.add_argument("--max-runners", type=int, default=10)
    parser.add_argument("--warm-runners", type=int, default=0)
    parser.add_argument("--node-hourly-cost-usd", type=float, default=0)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output", choices=["text", "json"], default="text")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    service = FleetService(Settings.from_env())
    report = service.simulate(
        SimulationRequest(
            scenario=args.scenario,
            job_count=args.jobs,
            max_runners=args.max_runners,
            warm_runners=args.warm_runners,
            node_hourly_cost_usd=args.node_hourly_cost_usd,
            seed=args.seed,
        )
    )
    if args.output == "json":
        print(report.model_dump_json(indent=2))
        return
    print(f"Scenario: {report.request.scenario}")
    print(f"Jobs: {report.request.job_count}")
    print(f"Queue p95: {report.snapshot.queue_p95_seconds:.1f}s")
    print(f"Failed startups: {report.snapshot.failed_startups}")
    print(f"Cleanup failures: {report.snapshot.cleanup_failures}")
    print(f"SLO passed: {report.slo.passed}")
    print(f"Breaches: {', '.join(report.slo.breached) or 'none'}")
    print(
        "Estimated runner compute cost: "
        f"${report.cost.estimated_runner_compute_cost_usd:.4f}"
    )


if __name__ == "__main__":
    main()

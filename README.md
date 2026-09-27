# Runner Fleet Reliability Platform

A portfolio platform for operating ephemeral GitHub Actions runner fleets with
SLOs, capacity policy, cost evidence, Prometheus metrics, incident simulation,
OpenTofu, Kubernetes, and a read-only MCP interface.

## Status

Version 0.1.0 is a local engineering scaffold. It does not yet represent a
production deployment, live AWS operation, or paying-customer system.

No cloud resources are created by the repository unless an operator explicitly
runs an OpenTofu apply.

## Current capabilities

- Deterministic simulations for baseline, burst, capacity loss, image pull
  failure, and GitHub API degradation
- Queue, startup, cleanup, and cost SLO evaluation
- Advisory capacity recommendations with explicit maximums
- SQLite report history and incident summaries
- Prometheus fleet metrics
- FastAPI control and evidence API
- Read-only MCP tools for fleet status, SLOs, incidents, capacity, and cost
- Tests and synthetic examples

## Safety boundary

MCP tools are intentionally read-only. They can explain fleet evidence and
recommend capacity, but they cannot create clusters, scale runners, apply
OpenTofu, or mutate Kubernetes resources.

## Local development

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -e ".[dev]"
.\.venv\Scripts\python -m pytest -q
.\.venv\Scripts\runner-fleet-simulate --scenario baseline --jobs 20
.\.venv\Scripts\runner-fleet-api
```

Open:

- API documentation: `http://127.0.0.1:8080/docs`
- Prometheus metrics: `http://127.0.0.1:8080/metrics`

Run the MCP server over stdio:

```powershell
.\.venv\Scripts\runner-fleet-mcp
```

Run the complete deterministic demonstration:

```powershell
.\scripts\run-demo.ps1
```

The demo compares a healthy baseline with a capacity-loss incident and writes
portfolio evidence under `evidence/generated`.

Current synthetic evidence:

- Baseline: queue p95 10 seconds, no startup failures, all SLOs pass
- Burst: queue and maximum-age SLOs fail
- Capacity loss: queue, startup-success, and maximum-age SLOs fail
- Image pull failure: queue and startup-success SLOs fail
- GitHub API degradation: queue and startup-success SLOs fail

See [the generated summary](evidence/generated/SUMMARY.md).

## Initial SLOs

| Signal | Target |
| --- | --- |
| Queue-to-start p95 | 90 seconds or less |
| Runner startup success | 99% or greater |
| Runner cleanup success | 100% |
| Maximum queue age | 300 seconds or less |

These are portfolio targets. They become claims only after a real deployment
produces supporting measurements.

## Roadmap

1. Validate the two kind-cluster development environment.
2. Deploy Actions Runner Controller and Prometheus.
3. Apply the temporary AWS EKS lab after explicit cost approval.
4. Add controlled chaos experiments against real Kubernetes resources.
5. Capture a cloud deployment, load test, incident timeline, cost report, and
   complete teardown.
6. Record a two-minute technical demonstration.

## Infrastructure

- `infra/bootstrap`: encrypted S3 state bucket and DynamoDB lock table
- `infra/aws`: VPC, public lab subnets, EKS 1.36, Spot managed nodes, ECR,
  CloudWatch control-plane logs, budget, and optional GitHub OIDC role
- `deploy/kind`: primary and recovery local clusters
- `deploy/arc`: controller and runner scale-set values
- `deploy/helm/runner-fleet-platform`: API, metrics, disruption budget,
  ServiceMonitor, and SLO alerts

OpenTofu applies are intentionally absent from CI. CI formats and validates the
configuration only.

## Documentation

- [Architecture](docs/ARCHITECTURE.md)
- [SLOs](docs/SLO.md)
- [Incident runbook](docs/RUNBOOK.md)
- [Security model](docs/SECURITY.md)
- [Cost model](docs/COST.md)
- [Architecture decisions](docs/DECISIONS.md)
- [MCP interface](docs/MCP.md)
- [Temporary AWS lab procedure](docs/AWS_LAB.md)
- [Synthetic incident review](evidence/sample-incident-review.md)

## Independence

This is a personal, unofficial clean-room project based only on public
documentation and synthetic data. It contains no employer source code,
customer data, internal configurations, support cases, or credentials.

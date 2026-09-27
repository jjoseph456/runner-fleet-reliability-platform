# Evidence

`generated/` is produced by:

```powershell
.\.venv\Scripts\python scripts\generate-evidence.py
```

Generated reports are deterministic simulations. They are not evidence of a
live Kubernetes or AWS deployment.

Live evidence must be stored separately and include:

- OpenTofu plan and apply identifiers
- Cluster and node versions
- ARC and runner image versions
- Workload definition and timestamps
- Prometheus queries and dashboard captures
- Alert and incident timeline
- Cost assumptions and AWS billing evidence
- OpenTofu destroy output and a post-destroy resource check

Never include credentials, account numbers, private repository names, customer
data, or employer configuration.

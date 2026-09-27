# Cost Model

The local simulator estimates only runner compute from an operator-supplied
hourly assumption.

It explicitly excludes:

- EKS control-plane charges
- Worker-node root volumes
- Public IPv4 charges
- ECR storage
- CloudWatch ingestion and retention
- Network transfer
- Cross-AZ traffic
- Remote-state storage

## Guardrails

- Default AWS Budget: $25 monthly
- Spot worker nodes
- Node group minimum of one and maximum of four
- No NAT Gateway
- Seven-day control-plane log retention
- ECR retains only ten images
- Every lab session ends with an explicit destroy command and evidence check

Before deployment, create an AWS Pricing Calculator estimate and replace
synthetic compute assumptions with current regional prices.

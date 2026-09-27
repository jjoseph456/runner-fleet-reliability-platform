# Architecture Decisions

## Use ARC rather than build another Kubernetes runner autoscaler

GitHub recommends Actions Runner Controller for Kubernetes-based autoscaling.
This project adds policy, observability, SLO, cost, incident, and MCP layers
around ARC instead of reimplementing its runner lifecycle.

## Keep MCP read-only

Natural-language access is useful for investigation, but infrastructure
mutation requires deterministic validation, review, and normal deployment
controls. MCP therefore exposes evidence and recommendations only.

## Begin in one AWS region

One measured region proves more than two unreliable regions. Multi-region
traffic and disaster recovery remain a later milestone after single-region
SLO, cleanup, and cost behavior are demonstrated.

## Avoid NAT Gateway in the portfolio lab

Public worker subnets reduce lab cost. This is documented as a portfolio-lab
tradeoff, not a recommended production topology.

# Security Model

## Controls

- Ephemeral, single-job runner design
- GitHub App or short-lived OIDC credentials
- No long-lived cloud keys in GitHub
- Immutable ECR tags and scan-on-push
- Restricted EKS public API CIDRs
- Non-root control-plane container
- Read-only MCP tools
- Explicit OpenTofu apply and destroy steps
- External runner log retention before production use

## Lab compromises

The temporary portfolio lab uses public worker subnets to avoid NAT Gateway
cost. A production design should use private subnets, controlled egress,
multi-AZ NAT or an approved alternative, VPC endpoints, and stronger network
segmentation.

The sample GitHub deployment role can publish images and describe the cluster;
it cannot apply OpenTofu or mutate Kubernetes by itself.

## Prohibited content

Do not include employer credentials, customer repositories, production logs,
internal runner labels, private images, or support cases.

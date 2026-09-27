# Temporary AWS Lab Procedure

This procedure is documentation only. Do not run `tofu apply` until the
operator has reviewed the AWS Pricing Calculator estimate, configured a
budget, and explicitly approved cloud creation.

## Prerequisites

- Personal AWS account
- AWS CLI authenticated without committing credentials
- Trusted public IP in CIDR form
- OpenTofu 1.10 or newer
- Confirmed standard-support EKS version

## 1. Estimate and budget

Estimate:

- EKS control plane
- Two Spot worker nodes
- EBS root volumes
- Public IPv4 addresses
- ECR
- CloudWatch logs
- Data transfer

Create a $25 monthly AWS Budget before the lab.

## 2. Bootstrap remote state

```powershell
Set-Location infra\bootstrap
tofu init
tofu plan -out bootstrap.tfplan
tofu apply bootstrap.tfplan
tofu output
```

Copy the bucket and table outputs into `infra/aws/backend.hcl`, which is
gitignored because it is environment-specific.

## 3. Prepare lab variables

```powershell
Copy-Item infra\aws\lab.tfvars.example infra\aws\lab.tfvars
Copy-Item infra\aws\backend.hcl.example infra\aws\backend.hcl
```

Replace all placeholders. Never use `0.0.0.0/0` for the EKS API endpoint.

## 4. Review the plan

```powershell
Set-Location infra\aws
tofu init -backend-config=backend.hcl
tofu fmt -check
tofu validate
tofu plan -var-file=lab.tfvars -out lab.tfplan
tofu show lab.tfplan
```

Review every billable resource before applying.

## 5. Create the temporary lab

```powershell
tofu apply lab.tfplan
aws eks update-kubeconfig --region us-east-1 --name runner-fleet-lab
kubectl get nodes
```

## 6. Capture evidence

- OpenTofu apply identifier
- EKS and node versions
- Node capacity and Spot events
- ARC controller, listener, and runner versions
- Fixed load profile
- Prometheus queries
- Alert and incident timeline
- Current AWS cost and forecast

## 7. Destroy and verify

```powershell
tofu plan -destroy -var-file=lab.tfvars -out destroy.tfplan
tofu apply destroy.tfplan
```

Then confirm that no unintended EKS clusters, EC2 instances, EBS volumes,
public IPv4 addresses, load balancers, or ECR images remain. Retain the remote
state resources until the portfolio lab is retired intentionally.

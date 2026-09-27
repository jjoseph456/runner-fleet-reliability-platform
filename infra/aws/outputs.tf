output "cluster_name" {
  value = aws_eks_cluster.lab.name
}

output "cluster_endpoint" {
  value = aws_eks_cluster.lab.endpoint
}

output "ecr_repository_url" {
  value = aws_ecr_repository.platform.repository_url
}

output "github_deploy_role_arn" {
  value = try(aws_iam_role.github_deploy[0].arn, null)
}

output "destroy_command" {
  value = "tofu destroy -var-file=lab.tfvars"
}

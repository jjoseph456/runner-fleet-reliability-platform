variable "project_name" {
  description = "Name used for AWS resources."
  type        = string
  default     = "runner-fleet-lab"
}

variable "aws_region" {
  description = "AWS region for the temporary lab."
  type        = string
  default     = "us-east-1"
}

variable "kubernetes_version" {
  description = "EKS Kubernetes version in standard support."
  type        = string
  default     = "1.36"
}

variable "allowed_api_cidrs" {
  description = "CIDRs allowed to reach the public EKS API endpoint. Use a trusted /32."
  type        = list(string)

  validation {
    condition     = length(var.allowed_api_cidrs) > 0 && !contains(var.allowed_api_cidrs, "0.0.0.0/0")
    error_message = "Provide at least one restricted CIDR; 0.0.0.0/0 is not allowed."
  }
}

variable "node_instance_types" {
  description = "Spot instance types for the temporary managed node group."
  type        = list(string)
  default     = ["t3.medium"]
}

variable "node_min_size" {
  type    = number
  default = 1
}

variable "node_desired_size" {
  type    = number
  default = 2
}

variable "node_max_size" {
  type    = number
  default = 4
}

variable "budget_limit_usd" {
  description = "Monthly portfolio-lab budget threshold."
  type        = number
  default     = 25
}

variable "budget_email" {
  description = "Optional email for AWS Budget alerts."
  type        = string
  default     = ""
}

variable "github_repository" {
  description = "Optional owner/repository allowed to assume the deployment role."
  type        = string
  default     = ""
}

variable "create_github_oidc_provider" {
  description = "Create the account-level GitHub OIDC provider if one does not exist."
  type        = bool
  default     = false
}

variable "existing_github_oidc_provider_arn" {
  description = "Existing account-level GitHub OIDC provider ARN."
  type        = string
  default     = null
  nullable    = true
}

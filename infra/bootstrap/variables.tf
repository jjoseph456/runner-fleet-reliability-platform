variable "aws_region" {
  description = "AWS region for the remote-state resources."
  type        = string
  default     = "us-east-1"
}

variable "name_prefix" {
  description = "Prefix for the state bucket and lock table."
  type        = string
  default     = "runner-fleet-lab"
}

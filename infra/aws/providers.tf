provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project     = var.project_name
      Environment = "portfolio-lab"
      ManagedBy   = "OpenTofu"
      AutoDestroy = "true"
    }
  }
}

data "aws_availability_zones" "available" {
  state = "available"
}

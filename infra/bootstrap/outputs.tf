output "state_bucket" {
  description = "S3 bucket for the main environment backend."
  value       = aws_s3_bucket.state.id
}

output "lock_table" {
  description = "DynamoDB table used for state locking."
  value       = aws_dynamodb_table.locks.name
}

output "aws_region" {
  value = var.aws_region
}

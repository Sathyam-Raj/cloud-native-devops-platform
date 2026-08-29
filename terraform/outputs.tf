output "ecr_repository_url" {
  value = aws_ecr_repository.cloud_app.repository_url
}

output "github_actions_role_arn" {
  value = aws_iam_role.github_actions_ecr.arn
}
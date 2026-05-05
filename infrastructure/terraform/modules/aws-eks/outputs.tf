output "cluster_id" {
  value = aws_eks_cluster.main.id
}

output "cluster_name" {
  value = aws_eks_cluster.main.name
}

output "cluster_endpoint" {
  value = aws_eks_cluster.main.endpoint
}

output "cluster_ca_certificate" {
  value = aws_eks_cluster.main.certificate_authority[0].data
}

output "cluster_security_group_id" {
  value = aws_security_group.cluster.id
}

output "node_group_role_arn" {
  value = aws_iam_role.node_group.arn
}

output "oidc_provider_arn" {
  value = aws_iam_openid_connect_provider.cluster.arn
}

output "oidc_provider_url" {
  value = replace(aws_eks_cluster.main.identity[0].oidc[0].issuer, "https://", "")
}

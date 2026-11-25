resource "aws_eks_cluster" "this" {
  name     = "bw-${var.env}"
  role_arn = aws_iam_role.cluster.arn
  version  = "1.30"
  vpc_config { subnet_ids = var.subnet_ids }
}

resource "aws_eks_node_group" "default" {
  cluster_name    = aws_eks_cluster.this.name
  node_group_name = "default"
  node_role_arn   = aws_iam_role.node.arn
  subnet_ids      = var.subnet_ids
  instance_types  = ["m6g.large"]
  scaling_config {
    desired_size = var.node_count
    min_size     = var.node_count
    max_size     = var.node_count * 2
  }
}

resource "aws_iam_role" "cluster" {
  name               = "bw-${var.env}-eks-cluster"
  assume_role_policy = jsonencode({ Version = "2012-10-17", Statement = [{ Effect = "Allow",
    Principal = { Service = "eks.amazonaws.com" }, Action = "sts:AssumeRole" }] })
}

resource "aws_iam_role" "node" {
  name               = "bw-${var.env}-eks-node"
  assume_role_policy = jsonencode({ Version = "2012-10-17", Statement = [{ Effect = "Allow",
    Principal = { Service = "ec2.amazonaws.com" }, Action = "sts:AssumeRole" }] })
}

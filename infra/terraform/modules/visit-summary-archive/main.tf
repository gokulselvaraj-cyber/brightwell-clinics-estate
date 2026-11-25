# Signed AI visit summaries (written by services/visit-summary SummaryArchiver).
terraform {
  required_providers {
    aws = { source = "hashicorp/aws", configuration_aliases = [aws.dr] }
  }
}

resource "aws_s3_bucket" "archive" {
  bucket = var.env == "prod" ? "bw-visit-summaries-euw2" : "bw-${var.env}-visit-summaries"
}

resource "aws_s3_bucket_versioning" "archive" {
  bucket = aws_s3_bucket.archive.id
  versioning_configuration { status = "Enabled" }
}

resource "aws_s3_bucket_lifecycle_configuration" "archive" {
  bucket = aws_s3_bucket.archive.id
  rule {
    id     = "expire-2y"
    status = "Enabled"
    filter {}
    expiration { days = 730 }
  }
}

# DR copy. Added after INC-2291 (eu-west-2 S3 degradation, 2026-04-14).
resource "aws_s3_bucket" "replica" {
  count    = var.enable_dr ? 1 : 0
  provider = aws.dr
  bucket   = "bw-visit-summaries-dr-use1"
}

resource "aws_s3_bucket_versioning" "replica" {
  count    = var.enable_dr ? 1 : 0
  provider = aws.dr
  bucket   = aws_s3_bucket.replica[0].id
  versioning_configuration { status = "Enabled" }
}

resource "aws_s3_bucket_replication_configuration" "archive" {
  count  = var.enable_dr ? 1 : 0
  bucket = aws_s3_bucket.archive.id
  role   = aws_iam_role.replication[0].arn
  rule {
    id     = "all-signed-summaries"
    status = "Enabled"
    filter { prefix = "signed/" }
    destination {
      bucket        = aws_s3_bucket.replica[0].arn
      storage_class = "STANDARD_IA"
    }
    delete_marker_replication { status = "Disabled" }
  }
  depends_on = [aws_s3_bucket_versioning.archive]
}

resource "aws_iam_role" "replication" {
  count              = var.enable_dr ? 1 : 0
  name               = "bw-${var.env}-summary-replication"
  assume_role_policy = jsonencode({ Version = "2012-10-17", Statement = [{ Effect = "Allow",
    Principal = { Service = "s3.amazonaws.com" }, Action = "sts:AssumeRole" }] })
}

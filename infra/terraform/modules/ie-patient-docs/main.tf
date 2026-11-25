# Referral letters and documents for patients of Irish clinics: kept in eu-west-1 (Dublin).
resource "aws_s3_bucket" "docs" {
  bucket = "bw-${var.env}-ie-patient-docs"
}

resource "aws_s3_bucket_server_side_encryption_configuration" "docs" {
  bucket = aws_s3_bucket.docs.id
  rule {
    apply_server_side_encryption_by_default { sse_algorithm = "aws:kms" }
  }
}

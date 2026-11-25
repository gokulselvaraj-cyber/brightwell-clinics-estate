terraform {
  backend "s3" {
    bucket         = "bw-tfstate-test"
    key            = "platform/terraform.tfstate"
    region         = "eu-west-2"
    dynamodb_table = "bw-tf-locks"
    encrypt        = true
  }
}

terraform {
  required_version = ">= 1.8.0"
  required_providers {
    aws = { source = "hashicorp/aws", version = "5.80.0" }
  }
}

provider "aws" {
  region = "eu-west-2"
  default_tags { tags = { environment = "prod", owner = "team-platform", system = "brightwell" } }
}

provider "aws" {
  alias  = "ie"
  region = "eu-west-1"
}
# Disaster-recovery copy of signed visit summaries (INC-2291 follow-up, 2026-05)
provider "aws" {
  alias  = "us_dr"
  region = "us-east-1"
}

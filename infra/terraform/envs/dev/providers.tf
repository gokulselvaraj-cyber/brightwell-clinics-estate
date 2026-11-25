terraform {
  required_version = ">= 1.8.0"
  required_providers {
    aws = { source = "hashicorp/aws", version = "5.80.0" }
  }
}

provider "aws" {
  region = "eu-west-2"
  default_tags { tags = { environment = "dev", owner = "team-platform", system = "brightwell" } }
}

provider "aws" {
  alias  = "ie"
  region = "eu-west-1"
}

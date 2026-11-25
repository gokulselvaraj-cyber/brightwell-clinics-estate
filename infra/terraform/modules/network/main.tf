data "aws_availability_zones" "this" {}

resource "aws_vpc" "this" {
  cidr_block           = var.cidr_block
  enable_dns_hostnames = true
  tags                 = { Name = "bw-${var.env}" }
}

resource "aws_subnet" "private" {
  count             = 3
  vpc_id            = aws_vpc.this.id
  cidr_block        = cidrsubnet(var.cidr_block, 4, count.index)
  availability_zone = data.aws_availability_zones.this.names[count.index]
  tags              = { Name = "bw-${var.env}-private-${count.index}" }
}

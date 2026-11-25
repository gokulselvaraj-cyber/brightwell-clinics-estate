resource "aws_db_subnet_group" "this" {
  name       = "bw-${var.env}-${var.name}"
  subnet_ids = var.subnet_ids
}

resource "aws_db_instance" "this" {
  identifier                  = "bw-${var.env}-${var.name}"
  engine                      = "postgres"
  engine_version              = "15.10"
  instance_class              = var.instance_class
  allocated_storage           = 200
  storage_encrypted           = true
  multi_az                    = var.multi_az
  db_subnet_group_name        = aws_db_subnet_group.this.name
  username                    = "bw_owner"
  manage_master_user_password = true
  backup_retention_period     = 14
  deletion_protection         = var.env == "prod"
}

resource "aws_db_instance" "replica" {
  count               = var.env == "prod" && var.name == "appointments-db" ? 1 : 0
  identifier          = "bw-${var.env}-${var.name}-replica"
  replicate_source_db = aws_db_instance.this.identifier
  instance_class      = var.instance_class
}

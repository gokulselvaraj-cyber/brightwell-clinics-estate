module "network" {
  source     = "../../modules/network"
  env        = var.env
  cidr_block = var.cidr_block
}

module "eks" {
  source     = "../../modules/eks"
  env        = var.env
  subnet_ids = module.network.private_subnet_ids
  node_count = var.node_count
}

module "appointments_db" {
  source         = "../../modules/rds"
  env            = var.env
  name           = "appointments-db"
  instance_class = var.db_instance_class
  multi_az       = var.db_multi_az
  subnet_ids     = module.network.private_subnet_ids
}

module "reporting_db" {
  source         = "../../modules/rds"
  env            = var.env
  name           = "reporting"
  instance_class = "db.t4g.large"
  multi_az       = false
  subnet_ids     = module.network.private_subnet_ids
}

module "ie_patient_docs" {
  source    = "../../modules/ie-patient-docs"
  env       = var.env
  providers = { aws = aws.ie }
}
module "visit_summary_archive" {
  source    = "../../modules/visit-summary-archive"
  env       = var.env
  providers = { aws = aws, aws.dr = aws.us_dr }
}

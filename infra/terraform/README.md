# Terraform

AWS, one account per environment. UK workloads in **eu-west-2** (London); Irish patient data in
**eu-west-1** (Dublin). See docs/adr/ADR-0004-patient-data-residency.md.

`envs/<env>` composes the modules; state in S3 `bw-tfstate-<env>` (eu-west-2) with DynamoDB locking.

# Nightly reporting load failed

- Re-run from the failed task in Airflow; tasks are idempotent except `publish_to_warehouse`.
- `map_procedure_codes` KeyError: a new BWP code is missing from the reference module; add it and redeploy.
- The DAG must finish before 07:00 for the clinic dashboards.

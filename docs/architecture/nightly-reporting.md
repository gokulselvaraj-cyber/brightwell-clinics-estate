# Nightly reporting load

Airflow DAG `nightly_reporting_load`, 02:30 Europe/London. Source: the appointmentsdb read replica.
Target: `bwreporting` on `reporting.brightwell.internal`.

extract_appointments → load_staging → map_procedure_codes → transform_fact_visit → transform_noshow_flags
→ build_clinic_daily → build_dim_service_user → publish_to_warehouse

Dashboards (clinic DNA rate, late cancellations, revenue by band) read `rpt.agg_clinic_daily` and
`rpt.fact_visit`. Commissioning reports read `rpt.dim_service_user`.

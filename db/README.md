# appointmentsdb

PostgreSQL 15, schema `bw`. Migrations are Flyway (`migrations/V*__*.sql`), applied by the
`db-migrate` job in CI before appointments-api deploys. Reference data: `seed/reference_data.sql`
(clinics, specialties, clinicians, slot templates, runtime settings in `bw.app_setting`, closures).

Personal data lives in `bw.patient`, `bw.visit` (clinician notes) and `bw.visit_summary`.
Retention: `bw.purge_expired_records()` (V7), run weekly by the `weekly_retention_purge` DAG.

Roles: `bw_app` (appointments-api), `bw_summary` (visit-summary), `bw_reminders` (reminder-worker),
`bw_replica_reader` (reporting extract, read replica only).

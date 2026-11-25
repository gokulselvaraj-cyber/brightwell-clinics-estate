"""Swap the freshly built rpt tables into the reporting schema used by dashboards."""
from airflow.providers.postgres.hooks.postgres import PostgresHook

PUBLISHED = ["fact_visit", "agg_clinic_daily", "dim_service_user", "dim_clinic"]


def publish(conn_id: str, enabled: bool = True, **_) -> None:
    if not enabled:
        return
    hook = PostgresHook(postgres_conn_id=conn_id)
    for table in PUBLISHED:
        hook.run(f"select rpt.swap_published('{table}')")

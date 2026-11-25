"""Weekly retention purge on appointmentsdb (Sundays 04:00 Europe/London).

Calls bw.purge_expired_records() (db/migrations/V7__retention.sql) and logs the row counts.
"""
import pendulum
from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator

with DAG(
    dag_id="weekly_retention_purge",
    schedule="0 4 * * 0",
    start_date=pendulum.datetime(2025, 1, 5, tz="Europe/London"),
    catchup=False,
    tags=["retention", "gdpr"],
) as dag:
    purge_expired = PostgresOperator(task_id="purge_expired", postgres_conn_id="appointmentsdb_primary",
                                     sql="select * from bw.purge_expired_records();")

"""Load landed parquet files into rpt.stg_* (truncate + insert)."""
import pandas as pd
from airflow.providers.postgres.hooks.postgres import PostgresHook

TABLES = {"appointment": "stg_appointment", "patient": "stg_patient", "visit": "stg_visit"}


def load_staging(conn_id: str, ti=None, **_) -> None:
    paths = ti.xcom_pull(task_ids="extract_appointments")
    engine = PostgresHook(postgres_conn_id=conn_id).get_sqlalchemy_engine()
    with engine.begin() as conn:
        for name, table in TABLES.items():
            conn.exec_driver_sql(f"truncate rpt.{table}")
            pd.read_parquet(paths[name]).to_sql(table, conn, schema="rpt", if_exists="append", index=False)

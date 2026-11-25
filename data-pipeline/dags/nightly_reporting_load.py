"""Nightly reporting load: appointmentsdb (read replica) -> rpt staging -> facts/dims -> bwreporting.

Runs 02:30 Europe/London every day. Tasks:
extract_appointments >> load_staging >> map_procedure_codes >> transform_fact_visit
  >> transform_noshow_flags >> build_clinic_daily >> build_dim_service_user >> publish_to_warehouse
"""
from datetime import timedelta

import pendulum
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator

from bw_pipeline import extract, load, publish, tariffs
from bw_pipeline.config import load_config

CFG = load_config()
SQL = "/opt/airflow/dags/repo/data-pipeline/sql/transforms"

default_args = {"owner": "data-insight", "retries": 2, "retry_delay": timedelta(minutes=10)}

with DAG(
    dag_id="nightly_reporting_load",
    schedule="30 2 * * *",
    start_date=pendulum.datetime(2025, 1, 1, tz="Europe/London"),
    catchup=False,
    default_args=default_args,
    max_active_runs=1,
    tags=["reporting", "nightly"],
) as dag:
    extract_appointments = PythonOperator(
        task_id="extract_appointments", python_callable=extract.extract_appointments,
        op_kwargs={"conn_id": CFG["source_conn_id"], "lookback_days": CFG["extract_lookback_days"]})
    load_staging = PythonOperator(task_id="load_staging", python_callable=load.load_staging,
                                  op_kwargs={"conn_id": CFG["warehouse_conn_id"]})
    map_procedure_codes = PythonOperator(task_id="map_procedure_codes",
                                         python_callable=tariffs.map_staged_procedures,
                                         op_kwargs={"conn_id": CFG["warehouse_conn_id"]})
    transform_fact_visit = PostgresOperator(task_id="transform_fact_visit",
                                            postgres_conn_id=CFG["warehouse_conn_id"],
                                            sql=f"{SQL}/010_fact_visit.sql")
    transform_noshow_flags = PostgresOperator(task_id="transform_noshow_flags",
                                              postgres_conn_id=CFG["warehouse_conn_id"],
                                              sql=f"{SQL}/020_noshow_flags.sql")
    build_clinic_daily = PostgresOperator(task_id="build_clinic_daily",
                                          postgres_conn_id=CFG["warehouse_conn_id"],
                                          sql=f"{SQL}/030_agg_clinic_daily.sql")
    build_dim_service_user = PostgresOperator(task_id="build_dim_service_user",
                                              postgres_conn_id=CFG["warehouse_conn_id"],
                                              sql=f"{SQL}/040_dim_service_user.sql")
    publish_to_warehouse = PythonOperator(task_id="publish_to_warehouse", python_callable=publish.publish,
                                          op_kwargs={"conn_id": CFG["warehouse_conn_id"],
                                                     "enabled": CFG["publish"]})

    (extract_appointments >> load_staging >> map_procedure_codes >> transform_fact_visit
     >> transform_noshow_flags >> build_clinic_daily >> build_dim_service_user >> publish_to_warehouse)

"""Extract changed appointments, patients and visits from the appointmentsdb read replica."""
from pathlib import Path

import pandas as pd
from airflow.providers.postgres.hooks.postgres import PostgresHook

LANDING = Path("/opt/airflow/landing/appointments")

QUERIES = {
    "appointment": """
        select a.id, a.appointment_ref, a.patient_id, a.clinic_code, a.specialty_code, a.procedure_code,
               a.status, a.starts_at, a.booked_via, a.cancelled_at
          from bw.appointment a
         where a.starts_at >= now() - make_interval(days => %(days)s)
            or a.cancelled_at >= now() - make_interval(days => %(days)s)""",
    "patient": """
        select p.id, p.patient_ref, p.date_of_birth, p.postcode, p.eircode, p.home_clinic_code,
               p.last_attended_at
          from bw.patient p
         where p.id in (select patient_id from bw.appointment
                         where starts_at >= now() - make_interval(days => %(days)s))""",
    "visit": """
        select v.id, v.appointment_id, v.clinician_id, v.procedure_code, v.outcome, v.closed_at
          from bw.visit v where v.closed_at >= now() - make_interval(days => %(days)s)""",
}


def extract_appointments(conn_id: str, lookback_days: int, **context) -> dict:
    hook = PostgresHook(postgres_conn_id=conn_id)
    run = context["ds_nodash"]
    out = {}
    for name, sql in QUERIES.items():
        df = pd.read_sql(sql, hook.get_sqlalchemy_engine(), params={"days": lookback_days})
        path = LANDING / run / f"{name}.parquet"
        path.parent.mkdir(parents=True, exist_ok=True)
        df.to_parquet(path, index=False)
        out[name] = str(path)
    return out

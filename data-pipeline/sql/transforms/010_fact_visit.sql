-- transform_fact_visit: staged appointments (+ visits) -> rpt.fact_visit
INSERT INTO rpt.fact_visit (visit_key, attendee_id, clinic_code, specialty_code, procedure_code,
                            visit_date, status, tariff_band, tariff_price, is_late_cancel)
SELECT a.id,
       a.patient_id                          AS attendee_id,
       a.clinic_code,
       a.specialty_code,
       coalesce(v.procedure_code, a.procedure_code),
       (a.starts_at AT TIME ZONE 'Europe/London')::date,
       a.status,
       a.tariff_band,
       CASE WHEN a.status = 'SEEN' THEN a.tariff_price END,
       a.status = 'LATE_CANCELLED'
  FROM rpt.stg_appointment a
  LEFT JOIN rpt.stg_visit v ON v.appointment_id = a.id
ON CONFLICT (visit_key) DO UPDATE
   SET status = excluded.status, procedure_code = excluded.procedure_code,
       tariff_band = excluded.tariff_band, tariff_price = excluded.tariff_price,
       is_late_cancel = excluded.is_late_cancel;

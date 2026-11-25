-- Appointments whose patient row is missing in staging
SELECT a.id FROM rpt.stg_appointment a LEFT JOIN rpt.stg_patient p ON p.id = a.patient_id
 WHERE p.id IS NULL;

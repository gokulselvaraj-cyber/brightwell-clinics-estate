CREATE INDEX ix_appointment_patient ON bw.appointment (patient_id, starts_at);
CREATE INDEX ix_appointment_clinic_day ON bw.appointment (clinic_code, starts_at);
CREATE INDEX ix_slot_session ON bw.slot (clinic_session_id, starts_at);
CREATE INDEX ix_reminder_due ON bw.reminder_outbox (status, due_at);
CREATE INDEX ix_patient_identity ON bw.patient (family_name, date_of_birth);

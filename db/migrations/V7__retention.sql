-- Retention routine (records policy RP-2, approved by the Caldicott Guardian 2025-09):
--   * patients and their visits: 8 years after the last attendance (adults)
--   * AI visit summaries: 2 years after creation (the signed letter is kept in the visit record)
--   * reminder_outbox rows: 90 days
-- Children's records are out of scope here (handled manually until age 25).
CREATE OR REPLACE FUNCTION bw.purge_expired_records()
RETURNS TABLE (object text, deleted bigint) LANGUAGE plpgsql AS $$
DECLARE
    n bigint;
BEGIN
    DELETE FROM bw.reminder_outbox WHERE due_at < now() - interval '90 days';
    GET DIAGNOSTICS n = ROW_COUNT; object := 'reminder_outbox'; deleted := n; RETURN NEXT;

    DELETE FROM bw.visit_summary WHERE created_at < now() - interval '2 years';
    GET DIAGNOSTICS n = ROW_COUNT; object := 'visit_summary'; deleted := n; RETURN NEXT;

    WITH expired AS (
        SELECT p.id FROM bw.patient p
         WHERE coalesce(p.last_attended_at, p.created_at) < now() - interval '8 years'
           AND p.date_of_birth < (now() - interval '18 years')::date
    ), gone_visits AS (
        DELETE FROM bw.visit v USING bw.appointment a, expired e
         WHERE v.appointment_id = a.id AND a.patient_id = e.id RETURNING v.id
    )
    SELECT count(*) INTO n FROM gone_visits;
    object := 'visit'; deleted := n; RETURN NEXT;

    DELETE FROM bw.patient p
     WHERE coalesce(p.last_attended_at, p.created_at) < now() - interval '8 years'
       AND p.date_of_birth < (now() - interval '18 years')::date
       AND NOT EXISTS (SELECT 1 FROM bw.appointment a JOIN bw.visit v ON v.appointment_id = a.id
                        WHERE a.patient_id = p.id);
    GET DIAGNOSTICS n = ROW_COUNT; object := 'patient'; deleted := n; RETURN NEXT;
END $$;

CREATE TABLE bw.audit_log (
    id         bigserial PRIMARY KEY,
    table_name varchar(40) NOT NULL,
    row_id     bigint NOT NULL,
    action     char(1) NOT NULL,
    changed_by varchar(64) NOT NULL DEFAULT current_user,
    changed_at timestamptz NOT NULL DEFAULT now(),
    old_row    jsonb
);

CREATE OR REPLACE FUNCTION bw.audit_patient() RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
    INSERT INTO bw.audit_log (table_name, row_id, action, old_row)
    VALUES ('patient', OLD.id, left(TG_OP, 1), to_jsonb(OLD));
    RETURN NULL;
END $$;

CREATE TRIGGER trg_audit_patient AFTER UPDATE OR DELETE ON bw.patient
    FOR EACH ROW EXECUTE FUNCTION bw.audit_patient();

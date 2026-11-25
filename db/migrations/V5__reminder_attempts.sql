ALTER TABLE bw.reminder_outbox ADD COLUMN attempts int NOT NULL DEFAULT 0;
ALTER TABLE bw.reminder_outbox ADD COLUMN provider_message_id varchar(40);
ALTER TABLE bw.reminder_outbox DROP CONSTRAINT IF EXISTS reminder_outbox_status_check;
ALTER TABLE bw.reminder_outbox ADD CONSTRAINT reminder_outbox_status_check
    CHECK (status IN ('PENDING', 'SENDING', 'SENT', 'FAILED', 'CANCELLED'));

ALTER TABLE bw.referral ADD CONSTRAINT referral_urgency_check
    CHECK (urgency IN ('ROUTINE', 'SOON', 'URGENT'));
CREATE INDEX ix_referral_patient ON bw.referral (patient_id);

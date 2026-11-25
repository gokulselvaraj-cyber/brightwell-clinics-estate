-- Ireland clinics (2019): PPSN and Eircode
ALTER TABLE bw.patient ADD COLUMN ppsn varchar(9);
ALTER TABLE bw.patient ADD COLUMN eircode varchar(8);
COMMENT ON COLUMN bw.patient.ppsn IS 'PII: Irish personal public service number';
COMMENT ON COLUMN bw.patient.eircode IS 'PII';
ALTER TABLE bw.patient ADD CONSTRAINT patient_one_national_id CHECK (nhs_number IS NULL OR ppsn IS NULL);

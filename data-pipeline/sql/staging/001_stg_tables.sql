-- Staging tables in bwreporting (rebuilt each night by load_staging)
CREATE SCHEMA IF NOT EXISTS rpt;

CREATE TABLE IF NOT EXISTS rpt.stg_appointment (
    id               bigint PRIMARY KEY,
    appointment_ref  varchar(14) NOT NULL,
    patient_id       bigint NOT NULL,
    clinic_code      varchar(9) NOT NULL,
    specialty_code   varchar(4) NOT NULL,
    procedure_code   varchar(9),
    status           varchar(16) NOT NULL,
    starts_at        timestamptz NOT NULL,
    booked_via       varchar(10),
    cancelled_at     timestamptz,
    tariff_specialty varchar(4),
    tariff_band      varchar(2),
    tariff_price     numeric(8,2)
);

CREATE TABLE IF NOT EXISTS rpt.stg_patient (
    id               bigint PRIMARY KEY,
    patient_ref      varchar(16) NOT NULL,
    date_of_birth    date,
    postcode         varchar(8),
    eircode          varchar(8),
    home_clinic_code varchar(9),
    last_attended_at timestamptz
);

CREATE TABLE IF NOT EXISTS rpt.stg_visit (
    id             bigint PRIMARY KEY,
    appointment_id bigint NOT NULL,
    clinician_id   bigint,
    procedure_code varchar(9),
    outcome        varchar(12),
    closed_at      timestamptz
);

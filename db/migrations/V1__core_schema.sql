CREATE SCHEMA IF NOT EXISTS bw;

CREATE TABLE bw.specialty (
    code  varchar(4) PRIMARY KEY,
    name  varchar(60) NOT NULL
);

CREATE TABLE bw.clinic (
    code        varchar(9) PRIMARY KEY,
    name        varchar(80) NOT NULL,
    town        varchar(60) NOT NULL,
    nation      varchar(3) NOT NULL CHECK (nation IN ('ENG', 'SCO', 'WAL', 'IE')),
    timezone    varchar(32) NOT NULL,
    data_region varchar(12) NOT NULL CHECK (data_region IN ('eu-west-2', 'eu-west-1')),
    active      boolean NOT NULL DEFAULT true
);

CREATE TABLE bw.clinician (
    id                bigserial PRIMARY KEY,
    staff_ref         varchar(10) NOT NULL UNIQUE,
    display_name      varchar(80) NOT NULL,
    specialty_code    varchar(4) NOT NULL REFERENCES bw.specialty (code),
    home_clinic_code  varchar(9) NOT NULL REFERENCES bw.clinic (code),
    registration_body varchar(8) NOT NULL
);

-- Personal data. COMMENTs mark the columns for the record of processing.
CREATE TABLE bw.patient (
    id               bigserial PRIMARY KEY,
    patient_ref      varchar(16) NOT NULL UNIQUE,
    given_name       varchar(80) NOT NULL,
    family_name      varchar(80) NOT NULL,
    date_of_birth    date NOT NULL,
    nhs_number       varchar(10),
    phone            varchar(20),
    email            varchar(254),
    address_line1    varchar(120),
    postcode         varchar(8),
    home_clinic_code varchar(9) NOT NULL REFERENCES bw.clinic (code),
    last_attended_at timestamptz,
    created_at       timestamptz NOT NULL DEFAULT now()
);
COMMENT ON COLUMN bw.patient.nhs_number IS 'PII: national health identifier (UK)';
COMMENT ON COLUMN bw.patient.date_of_birth IS 'PII';
COMMENT ON COLUMN bw.patient.phone IS 'PII: used for SMS reminders';
COMMENT ON COLUMN bw.patient.address_line1 IS 'PII';

CREATE TABLE bw.referral (
    id                bigserial PRIMARY KEY,
    patient_id        bigint NOT NULL REFERENCES bw.patient (id),
    referrer_name     varchar(120) NOT NULL,
    referrer_org_code varchar(12) NOT NULL,
    specialty_code    varchar(4) NOT NULL REFERENCES bw.specialty (code),
    urgency           varchar(8) NOT NULL DEFAULT 'ROUTINE',
    received_on       date NOT NULL
);

CREATE TABLE bw.clinic_session (
    id             bigserial PRIMARY KEY,
    clinic_code    varchar(9) NOT NULL REFERENCES bw.clinic (code),
    clinician_id   bigint NOT NULL REFERENCES bw.clinician (id),
    room           varchar(10) NOT NULL,
    session_date   date NOT NULL,
    starts         time NOT NULL,
    ends           time NOT NULL,
    specialty_code varchar(4) NOT NULL REFERENCES bw.specialty (code)
);

CREATE TABLE bw.slot (
    id                bigserial PRIMARY KEY,
    clinic_session_id bigint NOT NULL REFERENCES bw.clinic_session (id) ON DELETE CASCADE,
    starts_at         timestamptz NOT NULL,
    length_minutes    int NOT NULL,
    state             varchar(8) NOT NULL DEFAULT 'OPEN'
                      CHECK (state IN ('OPEN', 'HELD', 'BOOKED', 'BLOCKED')),
    held_until        timestamptz
);

CREATE TYPE bw.appointment_status AS ENUM
    ('BOOKED', 'CANCELLED', 'LATE_CANCELLED', 'ARRIVED', 'SEEN', 'NO_SHOW');

CREATE TABLE bw.appointment (
    id              bigserial PRIMARY KEY,
    appointment_ref varchar(14) NOT NULL UNIQUE,
    patient_id      bigint NOT NULL REFERENCES bw.patient (id),
    slot_id         bigint NOT NULL UNIQUE REFERENCES bw.slot (id),
    clinic_code     varchar(9) NOT NULL REFERENCES bw.clinic (code),
    specialty_code  varchar(4) NOT NULL REFERENCES bw.specialty (code),
    procedure_code  varchar(9),
    referral_id     bigint REFERENCES bw.referral (id),
    status          bw.appointment_status NOT NULL DEFAULT 'BOOKED',
    starts_at       timestamptz NOT NULL,
    booked_via      varchar(10) NOT NULL DEFAULT 'PORTAL',
    cancelled_at    timestamptz
);

CREATE TABLE bw.check_in (
    id             bigserial PRIMARY KEY,
    appointment_id bigint NOT NULL UNIQUE REFERENCES bw.appointment (id),
    checked_in_at  timestamptz NOT NULL DEFAULT now(),
    channel        varchar(10) NOT NULL
);

CREATE TABLE bw.visit (
    id              bigserial PRIMARY KEY,
    appointment_id  bigint NOT NULL UNIQUE REFERENCES bw.appointment (id),
    clinician_id    bigint NOT NULL REFERENCES bw.clinician (id),
    procedure_code  varchar(9),
    clinician_notes text,
    outcome         varchar(12),
    closed_at       timestamptz
);
COMMENT ON COLUMN bw.visit.clinician_notes IS 'PII + health data (special category)';

CREATE TABLE bw.reminder_outbox (
    id             bigserial PRIMARY KEY,
    appointment_id bigint NOT NULL REFERENCES bw.appointment (id),
    channel        varchar(6) NOT NULL,
    due_at         timestamptz NOT NULL,
    status         varchar(8) NOT NULL DEFAULT 'PENDING'
);

CREATE TABLE bw.app_setting (
    key         varchar(64) PRIMARY KEY,
    value       varchar(200) NOT NULL,
    description varchar(200)
);

CREATE TABLE bw.slot_template (
    clinic_code    varchar(9) NOT NULL REFERENCES bw.clinic (code),
    weekday        smallint NOT NULL CHECK (weekday BETWEEN 1 AND 6),
    starts         time NOT NULL,
    length_minutes int NOT NULL,
    specialty_code varchar(4) NOT NULL REFERENCES bw.specialty (code),
    room           varchar(10) NOT NULL,
    PRIMARY KEY (clinic_code, weekday, starts, room)
);

CREATE TABLE bw.clinic_procedure (
    clinic_code    varchar(9) NOT NULL REFERENCES bw.clinic (code),
    procedure_code varchar(9) NOT NULL,
    self_pay       boolean NOT NULL DEFAULT true,
    note           varchar(80),
    PRIMARY KEY (clinic_code, procedure_code)
);

CREATE TABLE bw.clinic_closure (
    clinic_code varchar(9) REFERENCES bw.clinic (code),
    nation      varchar(3),
    closed_on   date NOT NULL,
    reason      varchar(80) NOT NULL
);

-- Published reporting model in bwreporting (dashboards read these)
CREATE TABLE IF NOT EXISTS rpt.dim_clinic (
    clinic_code varchar(9) PRIMARY KEY,
    clinic_name varchar(80),
    town        varchar(60),
    nation      varchar(3),
    currency    char(3) NOT NULL DEFAULT 'GBP'
);

-- dim_service_user: one row per patient ("service user" in reporting language)
CREATE TABLE IF NOT EXISTS rpt.dim_service_user (
    service_user_key bigint PRIMARY KEY,
    patient_ref      varchar(16) NOT NULL,
    date_of_birth    date,
    age_band         varchar(8),
    postcode         varchar(8),
    postcode_district varchar(4),
    eircode_routing  varchar(3),
    home_clinic_code varchar(9),
    noshow_flag      boolean NOT NULL DEFAULT false
);

CREATE TABLE IF NOT EXISTS rpt.fact_visit (
    visit_key       bigint PRIMARY KEY,
    attendee_id     bigint NOT NULL REFERENCES rpt.dim_service_user (service_user_key),
    clinic_code     varchar(9) NOT NULL REFERENCES rpt.dim_clinic (clinic_code),
    specialty_code  varchar(4) NOT NULL,
    procedure_code  varchar(9),
    visit_date      date NOT NULL,
    status          varchar(16) NOT NULL,
    tariff_band     varchar(2),
    tariff_price    numeric(8,2),
    is_late_cancel  boolean NOT NULL DEFAULT false
);

CREATE TABLE IF NOT EXISTS rpt.agg_clinic_daily (
    clinic_code     varchar(9) NOT NULL,
    visit_date      date NOT NULL,
    booked          int NOT NULL,
    attended        int NOT NULL,
    no_shows        int NOT NULL,
    late_cancels    int NOT NULL,
    dna_rate        numeric(5,4),
    revenue         numeric(12,2),
    PRIMARY KEY (clinic_code, visit_date)
);

CREATE OR REPLACE FUNCTION rpt.swap_published(p_table text) RETURNS void LANGUAGE plpgsql AS $$
BEGIN
    EXECUTE format('ANALYZE rpt.%I', p_table);
    PERFORM pg_notify('rpt_published', p_table);
END $$;

-- build_dim_service_user: one row per patient seen in the staging window.
-- Full date of birth and full postcode are copied for the commissioning reports (DPIA-09 open action).
INSERT INTO rpt.dim_service_user (service_user_key, patient_ref, date_of_birth, age_band, postcode,
                                  postcode_district, eircode_routing, home_clinic_code)
SELECT p.id,
       p.patient_ref,
       p.date_of_birth,
       CASE WHEN age(p.date_of_birth) < interval '18 years' THEN '0-17'
            WHEN age(p.date_of_birth) < interval '40 years' THEN '18-39'
            WHEN age(p.date_of_birth) < interval '65 years' THEN '40-64'
            ELSE '65+' END,
       p.postcode,
       split_part(p.postcode, ' ', 1),
       left(p.eircode, 3),
       p.home_clinic_code
  FROM rpt.stg_patient p
ON CONFLICT (service_user_key) DO UPDATE
   SET postcode = excluded.postcode, postcode_district = excluded.postcode_district,
       eircode_routing = excluded.eircode_routing, home_clinic_code = excluded.home_clinic_code;

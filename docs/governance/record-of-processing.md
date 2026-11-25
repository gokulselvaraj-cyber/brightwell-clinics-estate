# Record of processing (UK GDPR Art. 30 / GDPR Art. 30)

Controller: Brightwell Clinics Ltd (UK) and Brightwell Clinics Ireland DAC.

| Activity | Data | Systems | Lawful basis | Retention | Processors |
|---|---|---|---|---|---|
| Booking and attendance | name, DOB, contact, NHS no./PPSN, address | appointments-api, bw.patient | Art. 6(1)(b), 9(2)(h) | 8 years after last attendance (adults) | AWS (eu-west-2, eu-west-1) |
| Reminders | first name, mobile number, appointment time | reminder-worker | Art. 6(1)(b) | outbox 90 days | RelayPost (UK) |
| Visit summaries | clinician notes (health data) | visit-summary, LLM gateway | Art. 9(2)(h) | 2 years (draft store) | internal LLM gateway |
| Reporting | patient_ref, DOB, postcode | data-pipeline, bwreporting | Art. 6(1)(f) | to be confirmed | AWS (eu-west-2) |

International transfers: **none**.
Open actions: DP-7 (names and DOB in free-text notes reach the LLM), DPIA-09 (full DOB and postcode in
rpt.dim_service_user).

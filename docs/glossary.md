# Glossary

| Term | Meaning |
|---|---|
| Patient | A person who books and attends. Table `bw.patient`. |
| Service user | Reporting name for a patient (`rpt.dim_service_user`). Same person as Patient. |
| Member | Portal name for a signed-in patient (`src/types/member.ts`). |
| Attendee | Column `attendee_id` in `rpt.fact_visit`: the patient. |
| Subject | visit-summary `subject_ref`: the patient of the visit. |
| Clinic session | A block of slots one clinician runs in one room. Not a login or database session. |
| Referral | A clinical referral from a GP or consultant. The portal's "refer a friend" code is marketing, not a referral. |
| DNA | Did not attend (a no-show). |
| Late cancellation | Cancelled inside the free-cancellation window. |
| BWP code | Brightwell procedure code (`BWP-01000` style); old `OPD-*` codes are remapped. |

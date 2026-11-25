# Patient data residency

Status: Accepted, 2023-02

## Decision
UK patient data stays in AWS eu-west-2 (London). Patient data for our clinics in Ireland is stored in eu-west-1 (Dublin) where the clinic or the patient requires it. **No patient data, including backups, replicas and AI outputs, is stored or processed outside the UK and the EU.** Any exception needs DPO sign-off and a transfer risk assessment.

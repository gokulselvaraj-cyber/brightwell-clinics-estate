# visit-summary

Drafts a plain-English visit summary for the patient letter from the clinician's notes. The clinician
always reviews and signs the draft before it is sent (clinical safety case CS-12).

- FastAPI, Python 3.11, port **8070**
- `POST /v1/summaries` (called by appointments-api `POST /v1/visits/{id}/summary`)
- `GET /v1/summaries/{summary_id}`
- Sends the prompt in `prompts/visit-summary.prompt.txt` plus the redacted notes to the internal LLM gateway
  (`LLM_GATEWAY_URL`, model `bw-clinsum-2`). Switch off with `VISIT_SUMMARY_LLM_ENABLED=false`
  (the service then returns a template-only draft).
- Stores drafts in `bw.visit_summary`; signed summaries are archived to S3 by `SummaryArchiver`.

Redaction: NHS numbers and PPSNs are removed before the call. See DPIA in `docs/governance/`.

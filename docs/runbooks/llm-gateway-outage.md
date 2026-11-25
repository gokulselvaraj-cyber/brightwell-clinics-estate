# LLM gateway outage

Symptom: `POST /v1/summaries` returns 502/504; clinicians see "Summary not available".
Action: set `VISIT_SUMMARY_LLM_ENABLED=false` in the visit-summary ConfigMap and restart; drafts fall back
to the template text. Tell clinical safety (CS-12 hazard H4).

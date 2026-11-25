# Draft visit summaries with an LLM

Status: Accepted, 2025-02

## Decision
visit-summary sends redacted clinician notes to the internal LLM gateway (hosted in eu-west-2) and stores a draft for the clinician to sign. Redaction removes national identifiers. Kill switch: VISIT_SUMMARY_LLM_ENABLED. Clinical safety case CS-12.

# New engineer onboarding

1. Request access to the `brightwell` GitHub org and the dev AWS account.
2. `make dev-up migrate seed` and run appointments-api locally.
3. Read ADR-0002 (outbox) and ADR-0004 (data residency) before touching reminders or storage.
4. Patient data in dev and test is synthetic only (`TEST-PATIENT-*`). Never copy production data down.

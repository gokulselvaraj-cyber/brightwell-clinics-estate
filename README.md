# Brightwell Clinics platform

Source for the Brightwell Clinics patient platform: outpatient clinics in England, Scotland, Wales and
Ireland. One repository, several deployables.

| Path | What |
|---|---|
| `services/appointments-api` | Booking, cancellation, check-in API (FastAPI, port 8000) |
| `services/visit-summary` | AI-drafted visit summaries via the LLM gateway (FastAPI, port 8070) |
| `services/reminder-worker` | SMS reminders from `bw.reminder_outbox` via RelayPost |
| `web/patient-portal` | Patient portal (React + TypeScript) |
| `data-pipeline` | Nightly reporting load (Airflow) into `bwreporting` |
| `db` | `appointmentsdb` migrations and reference data |
| `contracts` | OpenAPI and JSON Schema |
| `infra` | Terraform (AWS) and Kubernetes manifests |
| `vendor` | Third-party code we vendor (do not edit) |
| `retired` | Old applications kept for reference |
| `docs`, `ops` | Documentation, runbooks, alerts, SLOs |

Getting started: `make dev-up migrate seed`, then see each component's README.
Ownership: see `CODEOWNERS` and `catalog-info.yaml`.

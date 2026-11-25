# appointments-api

Booking, cancellation and check-in API for Brightwell Clinics. Python 3.11, FastAPI, SQLAlchemy 2,
PostgreSQL 15 (`appointmentsdb`, schema `bw`). Listens on port **8000**.

## Endpoints
| Method | Path | Role |
|---|---|---|
| GET | `/v1/clinics` | public |
| GET | `/v1/clinics/{clinic_code}/slots` | public |
| POST | `/v1/appointments` | PATIENT, RECEPTION |
| GET | `/v1/appointments/{appointment_id}` | PATIENT (own), RECEPTION |
| POST | `/v1/appointments/{appointment_id}/cancel` | PATIENT (own), RECEPTION |
| POST | `/v1/appointments/{appointment_id}/change` | PATIENT (own), RECEPTION |
| POST | `/v1/appointments/{appointment_id}/check-in` | PATIENT (own), RECEPTION |
| POST | `/v1/visits/{visit_id}/summary` | CLINICIAN |
| GET | `/v1/me/appointments` | PATIENT |
| GET | `/healthz`, `/readyz` | — |

## Booking flow
`book_appointment` → `BookingService.book` → `NoShowPolicy.is_restricted` → `SlotRepository.reserve` →
`PatientRepository.upsert` → `AppointmentRepository.insert` → `ReminderScheduler.schedule`.
Reminders are written to `bw.reminder_outbox` and sent by `services/reminder-worker`.

## Config
`config/application.yml` plus one file per environment (`application-{dev,test,prod}.yml`), selected with
`BW_ENV`. Environment variables override YAML (`BW_` prefix). Secrets come from the environment only
(`DB_PASSWORD`, `OIDC_CLIENT_SECRET`), injected from AWS Secrets Manager in the cluster.

## Running locally
```
make dev-up         # postgres via docker-compose
uvicorn brightwell_appointments.main:app --port 8000 --reload
pytest -q
```

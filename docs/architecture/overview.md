# Architecture overview

_Last reviewed: June 2024._

Brightwell's patient platform has three parts:

1. **appointments-api** (Python, FastAPI) on **MySQL 8** (`appointments` database). Handles booking,
   cancellation and check-in. Talks to the kiosk check-in app in each waiting room.
2. **patient-portal** (React). Patients book and cancel online.
3. **Reminders**: appointments-api emails a reminder 24 hours before each appointment through
   **SendLoop** (`https://api.sendloop.example/v1`).

Reporting: a nightly export to CSV is picked up by the finance team.

All services run in AWS eu-west-2.

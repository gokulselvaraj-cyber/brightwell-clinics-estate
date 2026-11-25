# Transactional outbox for reminders

Status: Accepted, 2024-01

## Decision
appointments-api writes reminder rows into bw.reminder_outbox in the booking transaction; a separate reminder-worker sends them by SMS through RelayPost. Email reminders through SendLoop are retired.

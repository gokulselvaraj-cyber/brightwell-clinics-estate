# reminder-worker

Polls `bw.reminder_outbox` every 60 seconds and sends SMS reminders through RelayPost
(vendored SDK in `vendor/relaypost-sms`). Templates are Jinja2 files in `templates/`.
Metrics on port 9102 (`bw_reminders_sent_total`, `bw_reminders_failed_total`).

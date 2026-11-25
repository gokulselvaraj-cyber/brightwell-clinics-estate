# Reminders not arriving

1. Check `bw_reminders_failed_total` on the clinic-ops dashboard.
2. `select status, count(*) from bw.reminder_outbox where due_at > now() - interval '1 day' group by 1;`
3. Many PENDING with attempts >= 4: RelayPost is rejecting. Check the RelayPost status page.
4. Restart with `ops/scripts/restart-reminders.sh <env>`.

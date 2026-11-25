from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock, patch

from brightwell_appointments.services.reminder_scheduler import ReminderScheduler


def test_two_reminders_for_future_appointment():
    with patch("brightwell_appointments.services.reminder_scheduler.get_settings") as gs:
        gs.return_value.reminders.offsets_hours = [48, 2]
        gs.return_value.reminders.channel = "SMS"
        sched = ReminderScheduler(MagicMock())
    appt = MagicMock(id=1, starts_at=datetime.now(timezone.utc) + timedelta(days=5))
    assert len(sched.schedule(appt)) == 2


def test_no_past_reminders():
    with patch("brightwell_appointments.services.reminder_scheduler.get_settings") as gs:
        gs.return_value.reminders.offsets_hours = [48, 2]
        gs.return_value.reminders.channel = "SMS"
        sched = ReminderScheduler(MagicMock())
    appt = MagicMock(id=1, starts_at=datetime.now(timezone.utc) + timedelta(hours=5))
    assert len(sched.schedule(appt)) == 1

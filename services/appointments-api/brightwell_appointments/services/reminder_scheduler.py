"""Writes reminder rows to bw.reminder_outbox; services/reminder-worker sends them."""
from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from ..models import Appointment, ReminderOutbox
from ..repositories.reminder_repository import ReminderRepository
from ..settings import get_settings


class ReminderScheduler:
    def __init__(self, session: Session):
        self.repo = ReminderRepository(session)
        self.cfg = get_settings().reminders

    def schedule(self, appt: Appointment) -> list[ReminderOutbox]:
        now = datetime.now(timezone.utc)
        rows = []
        for hours in self.cfg.offsets_hours:
            due = appt.starts_at - timedelta(hours=hours)
            if due > now:
                rows.append(ReminderOutbox(appointment_id=appt.id, channel=self.cfg.channel, due_at=due))
        self.repo.add_all(rows)
        return rows

    def reschedule(self, appt: Appointment) -> list[ReminderOutbox]:
        self.repo.cancel_pending(appt.id)
        return self.schedule(appt)

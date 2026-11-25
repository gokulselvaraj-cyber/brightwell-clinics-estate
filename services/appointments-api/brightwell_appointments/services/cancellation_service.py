"""Cancellation. Inside the late-cancel window (booking.late_cancel_hours) the appointment is
LATE_CANCELLED, which counts towards the clinic's late-cancellation fee report."""
from datetime import datetime, timedelta, timezone

from fastapi import HTTPException
from sqlalchemy.orm import Session

from ..models import AppointmentStatus
from ..repositories.appointment_repository import AppointmentRepository
from ..repositories.reminder_repository import ReminderRepository
from ..repositories.slot_repository import SlotRepository
from ..security import Principal
from ..settings import get_settings
from .booking_service import BookingService


class CancellationService:
    def __init__(self, session: Session):
        self.session = session
        self.appointments = AppointmentRepository(session)
        self.hours = get_settings().booking.late_cancel_hours

    def is_late(self, starts_at: datetime, now: datetime | None = None) -> bool:
        now = now or datetime.now(timezone.utc)
        return starts_at - now < timedelta(hours=self.hours)

    def cancel(self, appointment_id: int, reason: str | None, who: Principal):
        appt = self.appointments.get_for(appointment_id, who)
        if appt is None or appt.status != AppointmentStatus.BOOKED:
            raise HTTPException(409, "appointment cannot be cancelled")
        late = self.is_late(appt.starts_at)
        appt.status = AppointmentStatus.LATE_CANCELLED if late else AppointmentStatus.CANCELLED
        appt.cancelled_at = datetime.now(timezone.utc)
        SlotRepository(self.session).release(appt.slot_id)
        ReminderRepository(self.session).cancel_pending(appt.id)
        return BookingService(self.session)._view(appt)

"""Self check-in from the portal or at reception (journey: check-in).

Check-in opens `checkin.open_minutes_before` minutes before the start time. The value lives in
bw.app_setting (seeded by db/seed/reference_data.sql); 20 is only a fallback.
"""
from datetime import datetime, timedelta, timezone

from fastapi import HTTPException
from sqlalchemy.orm import Session

from ..models import AppointmentStatus, CheckIn
from ..repositories.appointment_repository import AppointmentRepository
from ..repositories.check_in_repository import CheckInRepository
from ..repositories.settings_repository import SettingsRepository
from ..schemas.check_in import CheckInResponse
from ..security import Principal

FALLBACK_OPEN_MINUTES = 20
GRACE_AFTER_START_MINUTES = 15


class CheckInService:
    def __init__(self, session: Session):
        self.session = session
        self.appointments = AppointmentRepository(session)
        self.checkins = CheckInRepository(session)
        self.settings = SettingsRepository(session)

    def window(self, starts_at: datetime) -> tuple[datetime, datetime]:
        minutes = self.settings.get_int("checkin.open_minutes_before", FALLBACK_OPEN_MINUTES)
        return (starts_at - timedelta(minutes=minutes),
                starts_at + timedelta(minutes=GRACE_AFTER_START_MINUTES))

    def check_in(self, appointment_id: int, channel: str, who: Principal) -> CheckInResponse:
        appt = self.appointments.get_for(appointment_id, who)
        if appt is None:
            raise HTTPException(404, "appointment not found")
        if appt.status != AppointmentStatus.BOOKED:
            raise HTTPException(409, f"cannot check in an appointment that is {appt.status.value}")
        opens, closes = self.window(appt.starts_at)
        now = datetime.now(timezone.utc)
        if not opens <= now <= closes:
            raise HTTPException(409, "check-in is not open for this appointment")
        row = self.checkins.insert(CheckIn(appointment_id=appt.id, channel=channel))
        appt.status = AppointmentStatus.ARRIVED
        position = self.checkins.queue_position(appt.clinic_code, appt.specialty_code, row.id)
        return CheckInResponse(appointment_ref=appt.appointment_ref, status=appt.status.value,
                               checked_in_at=row.checked_in_at, queue_position=position)

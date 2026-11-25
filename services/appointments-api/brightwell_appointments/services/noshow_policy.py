"""Online-booking restriction after repeated no-shows (attendance policy AP-3).

A patient with 3 or more NO_SHOW appointments in the last 365 days cannot book online; reception
can still book them. The reporting pipeline and the portal have their own copies of this rule.
"""
from datetime import datetime, timedelta, timezone

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from ..models import Appointment, AppointmentStatus

NO_SHOW_LIMIT = 3
LOOKBACK_DAYS = 365


class NoShowPolicy:
    def __init__(self, session: Session):
        self.session = session

    def count_recent(self, patient_id: int) -> int:
        since = datetime.now(timezone.utc) - timedelta(days=LOOKBACK_DAYS)
        stmt = (select(func.count()).select_from(Appointment)
                .where(Appointment.patient_id == patient_id)
                .where(Appointment.status == AppointmentStatus.NO_SHOW)
                .where(Appointment.starts_at >= since))
        return self.session.scalar(stmt) or 0

    def is_restricted(self, patient_id: int) -> bool:
        return self.count_recent(patient_id) >= NO_SHOW_LIMIT

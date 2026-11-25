from sqlalchemy import select
from sqlalchemy.orm import Session

from ..models import Appointment, Patient
from ..security import Principal


class AppointmentRepository:
    def __init__(self, session: Session):
        self.session = session

    def insert(self, appt: Appointment) -> Appointment:
        self.session.add(appt)
        self.session.flush()
        return appt

    def get_for(self, appointment_id: int, who: Principal) -> Appointment | None:
        stmt = select(Appointment).where(Appointment.id == appointment_id)
        if "RECEPTION" not in who.roles:
            stmt = stmt.join(Patient, Patient.id == Appointment.patient_id) \
                       .where(Patient.patient_ref == who.patient_ref)
        return self.session.scalars(stmt).first()

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..db import get_session
from ..models import Appointment, Patient
from ..schemas.appointment import AppointmentView
from ..security import Principal, require
from ..services.booking_service import BookingService

router = APIRouter(tags=["me"])


@router.get("/me/appointments", response_model=list[AppointmentView])
def my_appointments(session: Session = Depends(get_session), who: Principal = Depends(require("PATIENT"))):
    stmt = (select(Appointment).join(Patient, Patient.id == Appointment.patient_id)
            .where(Patient.patient_ref == who.patient_ref).order_by(Appointment.starts_at.desc()).limit(50))
    svc = BookingService(session)
    return [svc._view(a) for a in session.scalars(stmt)]

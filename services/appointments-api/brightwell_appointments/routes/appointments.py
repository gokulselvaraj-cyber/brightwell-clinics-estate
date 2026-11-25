from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..db import get_session
from ..schemas.appointment import AppointmentView, BookAppointmentRequest, CancelRequest, ChangeRequest
from ..security import Principal, require
from ..services.booking_service import BookingService, PatientRestricted, SlotUnavailable
from ..services.cancellation_service import CancellationService

router = APIRouter(tags=["appointments"])


@router.post("/appointments", response_model=AppointmentView, status_code=status.HTTP_201_CREATED)
def book_appointment(body: BookAppointmentRequest, session: Session = Depends(get_session),
                     who: Principal = Depends(require("PATIENT", "RECEPTION"))):
    try:
        return BookingService(session).book(body, who)
    except SlotUnavailable as exc:
        raise HTTPException(status.HTTP_409_CONFLICT, str(exc)) from exc
    except PatientRestricted as exc:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, str(exc)) from exc


@router.get("/appointments/{appointment_id}", response_model=AppointmentView)
def get_appointment(appointment_id: int, session: Session = Depends(get_session),
                    who: Principal = Depends(require("PATIENT", "RECEPTION"))):
    return BookingService(session).view(appointment_id, who)


@router.post("/appointments/{appointment_id}/cancel", response_model=AppointmentView)
def cancel_appointment(appointment_id: int, body: CancelRequest, session: Session = Depends(get_session),
                       who: Principal = Depends(require("PATIENT", "RECEPTION"))):
    return CancellationService(session).cancel(appointment_id, body.reason, who)


@router.post("/appointments/{appointment_id}/change", response_model=AppointmentView)
def change_appointment(appointment_id: int, body: ChangeRequest, session: Session = Depends(get_session),
                       who: Principal = Depends(require("PATIENT", "RECEPTION"))):
    return BookingService(session).change(appointment_id, body.new_slot_id, who)

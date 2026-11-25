from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..db import get_session
from ..schemas.check_in import CheckInResponse
from ..security import Principal, require
from ..services.check_in_service import CheckInService

router = APIRouter(tags=["check-in"])


@router.post("/appointments/{appointment_id}/check-in", response_model=CheckInResponse)
def check_in(appointment_id: int, session: Session = Depends(get_session),
             who: Principal = Depends(require("PATIENT", "RECEPTION"))):
    channel = "RECEPTION" if "RECEPTION" in who.roles else "PORTAL"
    return CheckInService(session).check_in(appointment_id, channel, who)

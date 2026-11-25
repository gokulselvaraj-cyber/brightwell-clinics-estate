from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..db import get_session
from ..schemas.slot import SlotView
from ..services.slot_finder import SlotFinder

router = APIRouter(tags=["clinics"])


@router.get("/clinics")
def list_clinics(session: Session = Depends(get_session)) -> list[dict]:
    return SlotFinder(session).clinics()


@router.get("/clinics/{clinic_code}/slots", response_model=list[SlotView])
def find_slots(clinic_code: str, specialty: str, on: date, session: Session = Depends(get_session)):
    return SlotFinder(session).open_slots(clinic_code, specialty, on)

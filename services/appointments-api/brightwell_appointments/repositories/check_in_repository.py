from sqlalchemy import text
from sqlalchemy.orm import Session

from ..models import CheckIn


class CheckInRepository:
    def __init__(self, session: Session):
        self.session = session

    def insert(self, row: CheckIn) -> CheckIn:
        self.session.add(row)
        self.session.flush()
        self.session.refresh(row)
        return row

    def queue_position(self, clinic_code: str, specialty_code: str, check_in_id: int) -> int:
        return self.session.execute(text("""
            select count(*) from bw.check_in ci join bw.appointment a on a.id = ci.appointment_id
             where a.clinic_code = :c and a.specialty_code = :s and a.status = 'ARRIVED'
               and ci.id <= :id and ci.checked_in_at::date = current_date"""),
            {"c": clinic_code, "s": specialty_code, "id": check_in_id}).scalar_one()

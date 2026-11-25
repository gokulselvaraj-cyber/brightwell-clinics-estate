from datetime import date

from sqlalchemy import text
from sqlalchemy.orm import Session


class SlotFinder:
    def __init__(self, session: Session):
        self.session = session

    def clinics(self) -> list[dict]:
        rows = self.session.execute(text(
            "select code, name, town, nation from bw.clinic where active order by town, name"))
        return [dict(r._mapping) for r in rows]

    def open_slots(self, clinic_code: str, specialty: str, on: date) -> list[dict]:
        rows = self.session.execute(text("""
            select s.id as slot_id, s.starts_at, s.length_minutes,
                   c.display_name as clinician_display_name, cs.specialty_code
              from bw.slot s
              join bw.clinic_session cs on cs.id = s.clinic_session_id
              join bw.clinician c on c.id = cs.clinician_id
             where cs.clinic_code = :clinic and cs.specialty_code = :spec
               and cs.session_date = :on and s.state = 'OPEN'
             order by s.starts_at"""), {"clinic": clinic_code, "spec": specialty, "on": on})
        return [dict(r._mapping) for r in rows]

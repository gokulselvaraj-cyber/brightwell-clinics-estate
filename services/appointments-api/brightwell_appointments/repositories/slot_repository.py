from datetime import datetime, timedelta, timezone

from sqlalchemy import text
from sqlalchemy.orm import Session

from ..models import Slot


class SlotRepository:
    def __init__(self, session: Session):
        self.session = session

    def reserve(self, slot_id: int, clinic_code: str) -> Slot | None:
        """Atomically move an OPEN (or expired HELD) slot to BOOKED."""
        row = self.session.execute(text("""
            update bw.slot s set state = 'BOOKED', held_until = null
              from bw.clinic_session cs
             where s.id = :id and cs.id = s.clinic_session_id and cs.clinic_code = :clinic
               and (s.state = 'OPEN' or (s.state = 'HELD' and s.held_until < now()))
            returning s.id"""), {"id": slot_id, "clinic": clinic_code}).first()
        return self.session.get(Slot, row.id) if row else None

    def hold(self, slot_id: int, minutes: int) -> None:
        until = datetime.now(timezone.utc) + timedelta(minutes=minutes)
        self.session.execute(text("update bw.slot set state='HELD', held_until=:u where id=:id and "
                                  "state='OPEN'"), {"u": until, "id": slot_id})

    def release(self, slot_id: int) -> None:
        self.session.execute(text("update bw.slot set state='OPEN' where id=:id"), {"id": slot_id})

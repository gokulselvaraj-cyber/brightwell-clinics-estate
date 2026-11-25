from sqlalchemy import update
from sqlalchemy.orm import Session

from ..models import ReminderOutbox


class ReminderRepository:
    def __init__(self, session: Session):
        self.session = session

    def add_all(self, rows: list[ReminderOutbox]) -> None:
        self.session.add_all(rows)
        self.session.flush()

    def cancel_pending(self, appointment_id: int) -> None:
        self.session.execute(update(ReminderOutbox)
                             .where(ReminderOutbox.appointment_id == appointment_id,
                                    ReminderOutbox.status == "PENDING")
                             .values(status="CANCELLED"))

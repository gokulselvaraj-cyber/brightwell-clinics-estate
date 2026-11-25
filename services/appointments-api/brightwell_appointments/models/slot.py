from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from ..db import Base


class Slot(Base):
    __tablename__ = "slot"
    __table_args__ = {"schema": "bw"}

    id: Mapped[int] = mapped_column(primary_key=True)
    clinic_session_id: Mapped[int] = mapped_column(ForeignKey("bw.clinic_session.id"))
    starts_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    length_minutes: Mapped[int] = mapped_column(Integer)
    state: Mapped[str] = mapped_column(String(8), default="OPEN")   # OPEN, HELD, BOOKED, BLOCKED
    held_until: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

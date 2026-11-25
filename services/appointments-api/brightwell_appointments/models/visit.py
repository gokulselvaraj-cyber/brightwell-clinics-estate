from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from ..db import Base


class Visit(Base):
    """A clinical encounter: created when the clinician opens an ARRIVED appointment."""
    __tablename__ = "visit"
    __table_args__ = {"schema": "bw"}

    id: Mapped[int] = mapped_column(primary_key=True)
    appointment_id: Mapped[int] = mapped_column(ForeignKey("bw.appointment.id"), unique=True)
    clinician_id: Mapped[int] = mapped_column(ForeignKey("bw.clinician.id"))
    procedure_code: Mapped[str | None] = mapped_column(String(8))
    clinician_notes: Mapped[str | None] = mapped_column(Text)
    outcome: Mapped[str | None] = mapped_column(String(12))
    closed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

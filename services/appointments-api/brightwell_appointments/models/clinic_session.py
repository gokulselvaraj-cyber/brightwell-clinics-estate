"""A ClinicSession is a block of consecutive slots one clinician runs in one room
(e.g. Tuesday 09:00-12:30 dermatology). Not to be confused with the database Session in db.py."""
from datetime import date, time

from sqlalchemy import Date, ForeignKey, String, Time
from sqlalchemy.orm import Mapped, mapped_column

from ..db import Base


class ClinicSession(Base):
    __tablename__ = "clinic_session"
    __table_args__ = {"schema": "bw"}

    id: Mapped[int] = mapped_column(primary_key=True)
    clinic_code: Mapped[str] = mapped_column(ForeignKey("bw.clinic.code"))
    clinician_id: Mapped[int] = mapped_column(ForeignKey("bw.clinician.id"))
    room: Mapped[str] = mapped_column(String(10))
    session_date: Mapped[date] = mapped_column(Date)
    starts: Mapped[time] = mapped_column(Time)
    ends: Mapped[time] = mapped_column(Time)
    specialty_code: Mapped[str] = mapped_column(String(4))

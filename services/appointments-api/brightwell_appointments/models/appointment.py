import enum
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from ..db import Base


class AppointmentStatus(str, enum.Enum):
    BOOKED = "BOOKED"
    CANCELLED = "CANCELLED"
    LATE_CANCELLED = "LATE_CANCELLED"
    ARRIVED = "ARRIVED"
    SEEN = "SEEN"
    NO_SHOW = "NO_SHOW"


class Appointment(Base):
    __tablename__ = "appointment"
    __table_args__ = {"schema": "bw"}

    id: Mapped[int] = mapped_column(primary_key=True)
    appointment_ref: Mapped[str] = mapped_column(String(14), unique=True)
    patient_id: Mapped[int] = mapped_column(ForeignKey("bw.patient.id"))
    slot_id: Mapped[int] = mapped_column(ForeignKey("bw.slot.id"), unique=True)
    clinic_code: Mapped[str] = mapped_column(String(9))
    specialty_code: Mapped[str] = mapped_column(String(4))
    procedure_code: Mapped[str | None] = mapped_column(String(8))
    referral_id: Mapped[int | None] = mapped_column(ForeignKey("bw.referral.id"))
    status: Mapped[AppointmentStatus] = mapped_column(Enum(AppointmentStatus, name="appointment_status",
                                                           schema="bw"), default=AppointmentStatus.BOOKED)
    starts_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    booked_via: Mapped[str] = mapped_column(String(10), default="PORTAL")
    cancelled_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

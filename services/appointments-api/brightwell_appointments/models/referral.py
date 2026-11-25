"""A clinical referral: a GP or consultant asks Brightwell to see a patient.

Unrelated to the portal's marketing "Referral" (refer-a-friend codes) in web/patient-portal.
"""
from datetime import date

from sqlalchemy import Date, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from ..db import Base


class Referral(Base):
    __tablename__ = "referral"
    __table_args__ = {"schema": "bw"}

    id: Mapped[int] = mapped_column(primary_key=True)
    patient_id: Mapped[int] = mapped_column(ForeignKey("bw.patient.id"))
    referrer_name: Mapped[str] = mapped_column(String(120))
    referrer_org_code: Mapped[str] = mapped_column(String(12))
    specialty_code: Mapped[str] = mapped_column(String(4))
    urgency: Mapped[str] = mapped_column(String(8))    # ROUTINE, SOON, URGENT
    received_on: Mapped[date] = mapped_column(Date)

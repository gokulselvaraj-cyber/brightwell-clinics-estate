"""A person who books and attends appointments.

Personal data (UK GDPR special category when combined with visits). The reporting pipeline calls the
same person a ServiceUser (rpt.dim_service_user); the portal calls them a Member.
"""
from datetime import date, datetime

from sqlalchemy import Date, DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column

from ..db import Base


class Patient(Base):
    __tablename__ = "patient"
    __table_args__ = {"schema": "bw"}

    id: Mapped[int] = mapped_column(primary_key=True)
    patient_ref: Mapped[str] = mapped_column(String(16), unique=True)   # BWP000123456
    given_name: Mapped[str] = mapped_column(String(80))
    family_name: Mapped[str] = mapped_column(String(80))
    date_of_birth: Mapped[date] = mapped_column(Date)
    nhs_number: Mapped[str | None] = mapped_column(String(10))   # UK patients
    ppsn: Mapped[str | None] = mapped_column(String(9))          # Irish patients
    phone: Mapped[str | None] = mapped_column(String(20))
    email: Mapped[str | None] = mapped_column(String(254))
    address_line1: Mapped[str | None] = mapped_column(String(120))
    postcode: Mapped[str | None] = mapped_column(String(8))
    eircode: Mapped[str | None] = mapped_column(String(8))
    home_clinic_code: Mapped[str] = mapped_column(String(9))
    last_attended_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    def masked_phone(self) -> str:
        return ("*" * 7 + self.phone[-3:]) if self.phone else ""

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from ..db import Base


class Clinician(Base):
    __tablename__ = "clinician"
    __table_args__ = {"schema": "bw"}

    id: Mapped[int] = mapped_column(primary_key=True)
    staff_ref: Mapped[str] = mapped_column(String(10), unique=True)
    display_name: Mapped[str] = mapped_column(String(80))
    specialty_code: Mapped[str] = mapped_column(String(4))
    home_clinic_code: Mapped[str] = mapped_column(ForeignKey("bw.clinic.code"))
    registration_body: Mapped[str] = mapped_column(String(8))   # GMC, HCPC, IMC, CORU

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from ..db import Base


class Clinic(Base):
    __tablename__ = "clinic"
    __table_args__ = {"schema": "bw"}

    code: Mapped[str] = mapped_column(String(9), primary_key=True)
    name: Mapped[str] = mapped_column(String(80))
    town: Mapped[str] = mapped_column(String(60))
    nation: Mapped[str] = mapped_column(String(3))     # ENG, SCO, WAL, IE
    timezone: Mapped[str] = mapped_column(String(32))
    data_region: Mapped[str] = mapped_column(String(12))

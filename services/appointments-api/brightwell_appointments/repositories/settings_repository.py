"""Reads runtime settings from bw.app_setting (key/value, seeded by db/seed/reference_data.sql)."""
from sqlalchemy import text
from sqlalchemy.orm import Session


class SettingsRepository:
    def __init__(self, session: Session):
        self.session = session

    def get(self, key: str) -> str | None:
        return self.session.execute(text("select value from bw.app_setting where key = :k"),
                                    {"k": key}).scalar_one_or_none()

    def get_int(self, key: str, default: int) -> int:
        value = self.get(key)
        return int(value) if value is not None else default

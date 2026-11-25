from datetime import datetime

from pydantic import BaseModel


class SlotView(BaseModel):
    slot_id: int
    starts_at: datetime
    length_minutes: int
    clinician_display_name: str
    specialty_code: str

from datetime import datetime

from pydantic import BaseModel


class CheckInResponse(BaseModel):
    appointment_ref: str
    status: str
    checked_in_at: datetime
    queue_position: int | None = None

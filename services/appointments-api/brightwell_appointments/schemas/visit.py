from pydantic import BaseModel


class SummaryAccepted(BaseModel):
    visit_id: int
    summary_id: str
    status: str = "DRAFT"

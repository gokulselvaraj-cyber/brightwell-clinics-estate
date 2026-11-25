from pydantic import BaseModel


class SummaryRequest(BaseModel):
    visit_id: int
    subject_ref: str            # the patient, as "appt:<appointment id>"
    procedure_code: str | None = None
    clinician_notes: str
    requested_by: str


class SummaryDraft(BaseModel):
    summary_id: str
    visit_id: int
    status: str                 # DRAFT, SIGNED, REJECTED
    text: str
    model: str | None = None

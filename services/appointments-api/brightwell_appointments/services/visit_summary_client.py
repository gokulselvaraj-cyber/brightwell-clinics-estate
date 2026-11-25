"""HTTP client for services/visit-summary (POST /v1/summaries)."""
import httpx

from ..models import Visit
from ..settings import get_settings


class VisitSummaryClient:
    def __init__(self):
        cfg = get_settings().visit_summary
        self.base = cfg.url.rstrip("/")
        self.timeout = cfg.timeout_seconds

    def request(self, visit: Visit, requested_by: str) -> str:
        payload = {
            "visit_id": visit.id,
            "subject_ref": f"appt:{visit.appointment_id}",
            "procedure_code": visit.procedure_code,
            "clinician_notes": visit.clinician_notes or "",
            "requested_by": requested_by,
        }
        resp = httpx.post(f"{self.base}/v1/summaries", json=payload, timeout=self.timeout)
        resp.raise_for_status()
        return resp.json()["summary_id"]

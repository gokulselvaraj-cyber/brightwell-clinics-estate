from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from ..db import get_session
from ..repositories.visit_repository import VisitRepository
from ..schemas.visit import SummaryAccepted
from ..security import Principal, require
from ..services.visit_summary_client import VisitSummaryClient

router = APIRouter(tags=["visits"])


@router.post("/visits/{visit_id}/summary", response_model=SummaryAccepted,
             status_code=status.HTTP_202_ACCEPTED)
def request_visit_summary(visit_id: int, session: Session = Depends(get_session),
                          who: Principal = Depends(require("CLINICIAN"))):
    visit = VisitRepository(session).get(visit_id)
    summary_id = VisitSummaryClient().request(visit, requested_by=who.subject)
    return SummaryAccepted(visit_id=visit_id, summary_id=summary_id)

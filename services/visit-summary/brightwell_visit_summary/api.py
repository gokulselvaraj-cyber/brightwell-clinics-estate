from fastapi import APIRouter, HTTPException, status

from .models import SummaryDraft, SummaryRequest
from .summary_repository import SummaryRepository
from .summary_service import SummaryService

router = APIRouter(prefix="/v1")


@router.post("/summaries", response_model=SummaryDraft, status_code=status.HTTP_201_CREATED)
def create_summary(req: SummaryRequest) -> SummaryDraft:
    return SummaryService().summarise(req)


@router.get("/summaries/{summary_id}", response_model=SummaryDraft)
def get_summary(summary_id: str) -> SummaryDraft:
    draft = SummaryRepository().get(summary_id)
    if draft is None:
        raise HTTPException(404, "summary not found")
    return draft


@router.post("/summaries/{summary_id}/sign", response_model=SummaryDraft)
def sign_summary(summary_id: str) -> SummaryDraft:
    return SummaryService().sign(summary_id)

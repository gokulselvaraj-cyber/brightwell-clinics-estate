"""Journey hop: visit summary. notes -> redaction -> prompt -> LLM gateway -> bw.visit_summary."""
import uuid

from .archiver import SummaryArchiver
from .llm_gateway_client import LlmGatewayClient
from .models import SummaryDraft, SummaryRequest
from .prompt_builder import PromptBuilder
from .redaction import strip_identifiers
from .settings import get_settings
from .summary_repository import SummaryRepository

TEMPLATE_ONLY = ("Thank you for attending your appointment. Your clinician will write to you with "
                 "the outcome and any next steps.")


class SummaryService:
    def __init__(self):
        self.cfg = get_settings()
        self.repo = SummaryRepository()

    def summarise(self, req: SummaryRequest) -> SummaryDraft:
        summary_id = str(uuid.uuid4())
        if not self.cfg.visit_summary_llm_enabled:
            text, model = TEMPLATE_ONLY, None
        else:
            notes = strip_identifiers(req.clinician_notes)
            messages = PromptBuilder().build(notes, req.procedure_code)
            text, model = LlmGatewayClient().complete(messages), self.cfg.llm_model
        draft = SummaryDraft(summary_id=summary_id, visit_id=req.visit_id, status="DRAFT", text=text,
                             model=model)
        self.repo.save(draft, requested_by=req.requested_by)
        return draft

    def sign(self, summary_id: str) -> SummaryDraft:
        draft = self.repo.mark_signed(summary_id)
        SummaryArchiver().archive(draft)
        return draft

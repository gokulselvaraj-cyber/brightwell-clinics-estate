from sqlalchemy import create_engine, text

from .models import SummaryDraft
from .settings import get_settings

_engine = None


def _eng():
    global _engine
    if _engine is None:
        _engine = create_engine(get_settings().database_url, pool_pre_ping=True)
    return _engine


class SummaryRepository:
    def save(self, d: SummaryDraft, requested_by: str) -> None:
        with _eng().begin() as c:
            c.execute(text("""insert into bw.visit_summary (summary_id, visit_id, status, summary_text,
                              model_version, requested_by) values (:s, :v, :st, :t, :m, :r)"""),
                      {"s": d.summary_id, "v": d.visit_id, "st": d.status, "t": d.text, "m": d.model,
                       "r": requested_by})

    def get(self, summary_id: str) -> SummaryDraft | None:
        with _eng().connect() as c:
            r = c.execute(text("select summary_id, visit_id, status, summary_text as text, model_version as model "
                               "from bw.visit_summary where summary_id = :s"), {"s": summary_id}).first()
        return SummaryDraft(**r._mapping) if r else None

    def mark_signed(self, summary_id: str) -> SummaryDraft:
        with _eng().begin() as c:
            c.execute(text("update bw.visit_summary set status='SIGNED', signed_at=now() where summary_id=:s"),
                      {"s": summary_id})
        return self.get(summary_id)

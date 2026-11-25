from fastapi import HTTPException
from sqlalchemy.orm import Session

from ..models import Visit


class VisitRepository:
    def __init__(self, session: Session):
        self.session = session

    def get(self, visit_id: int) -> Visit:
        visit = self.session.get(Visit, visit_id)
        if visit is None:
            raise HTTPException(404, "visit not found")
        return visit

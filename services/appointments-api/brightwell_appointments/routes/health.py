from fastapi import APIRouter
from sqlalchemy import text

from ..db import engine

router = APIRouter()


@router.get("/healthz")
def healthz() -> dict:
    return {"status": "ok"}


@router.get("/readyz")
def readyz() -> dict:
    with engine.connect() as conn:
        conn.execute(text("select 1"))
    return {"status": "ready"}

"""Database engine and the request-scoped SQLAlchemy Session.

Note: `Session` here is a database session. A clinic's block of bookable slots is a
`ClinicSession` (models/clinic_session.py); the two are unrelated.
"""
from collections.abc import Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from .settings import get_settings


class Base(DeclarativeBase):
    pass


def _url() -> str:
    db = get_settings().database
    return f"postgresql+psycopg://{db.user}:{db.password}@{db.host}:{db.port}/{db.name}"


engine = create_engine(_url(), pool_size=get_settings().database.pool_size, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)


def get_session() -> Iterator[Session]:
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

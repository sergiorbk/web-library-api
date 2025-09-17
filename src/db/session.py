from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from contextlib import contextmanager
from typing import Generator

from src.config import get_database_url


# Get database URL from config
DATABASE_URL = get_database_url()

engine = create_engine(DATABASE_URL, echo=False, future=True)


# Create session factory
session_factory = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    future=True,
)

# Create scoped session for thread safety
SessionLocal = scoped_session(session_factory)


def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        SessionLocal.remove()


@contextmanager
def get_db_context() -> Generator:
    """Context manager for database session"""
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
        SessionLocal.remove()


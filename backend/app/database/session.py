"""
===============================================================================
Database Session Management Module

Purpose:
--------
This module creates one short-lived SQLAlchemy session for each API request.
A session is the safe working connection used by routes to read and write data.

Request lifecycle:
------------------
Request -> get_db() opens session -> route uses session -> session closes

Why this matters:
-----------------
Closing each session in the finally block prevents connection and resource leaks.
Future FastAPI routes will receive a session with Depends(get_db), so they never
need to manually create or remember to close their own database sessions.
===============================================================================
"""

from collections.abc import Generator

from sqlalchemy.orm import Session

from app.database.database import SessionLocal


def get_db() -> Generator[Session, None, None]:
    """Provide one database session and close it when the request ends."""
    database_session = SessionLocal()
    try:
        yield database_session
    finally:
        database_session.close()

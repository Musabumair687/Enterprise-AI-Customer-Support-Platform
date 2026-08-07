"""
===============================================================================
Database Connection Module

Purpose:
--------
This module is the single place where the backend connects to its database.
It reads the SQLite connection URL from config.py, creates the SQLAlchemy engine,
and provides database sessions for future API routes.

Flow:
-----
.env -> config.py -> SQLAlchemy engine -> SQLite database file

What is included now:
---------------------
1. A SQLite SQLAlchemy engine.
2. A session factory for safe, short-lived database sessions.
3. A get_db dependency for future FastAPI endpoints.
4. An initialization check that confirms the database can be reached.

What comes next:
----------------
The table definitions live in app/models/models.py. Alembic migrations create
and update those tables; this module only checks the database connection.
===============================================================================
"""

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from app.config import get_settings


settings = get_settings()

# SQLite needs this option because FastAPI may handle requests across threads.
engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False},
)

# Each request will later receive its own session from this factory.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def initialize_database() -> None:
    """Connect to SQLite and fail startup immediately if it is unavailable."""
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))

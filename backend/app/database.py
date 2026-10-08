"""Database configuration and session management."""

from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

from app.config import settings


def get_database_url() -> str:
    """Get database URL from settings."""
    return settings.database_url


def create_db_engine():
    """
    Create SQLAlchemy engine with appropriate configuration.

    For SQLite: Uses StaticPool and enables foreign keys.
    For Postgres: Uses default connection pooling.
    """
    db_url = get_database_url()

    # SQLite configuration
    if "sqlite" in db_url:
        engine = create_engine(
            db_url,
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
            echo=settings.database_echo,
        )

        # Enable foreign key support in SQLite
        @event.listens_for(engine, "connect")
        def set_sqlite_pragma(dbapi_conn, connection_record):
            cursor = dbapi_conn.cursor()
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()
    else:
        # Postgres or other database
        engine = create_engine(
            db_url,
            echo=settings.database_echo,
            pool_pre_ping=True,  # Test connections before using
        )

    return engine


# Create engine and session factory
engine = create_db_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Session:
    """
    Dependency for FastAPI routes to get database session.

    Yields:
        SQLAlchemy Session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

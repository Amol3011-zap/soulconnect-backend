import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

_engine = None
_SessionLocal = None


def get_engine():
    global _engine
    if _engine is None:
        db_url = os.getenv("DATABASE_URL")
        if not db_url:
            raise RuntimeError("DATABASE_URL environment variable is not set")
        print(f"[database] Connecting to: {db_url[:50]}...")
        _engine = create_engine(
            db_url,
            echo=False,
            pool_pre_ping=True,
            pool_recycle=3600
        )
    return _engine


def get_session_local():
    global _SessionLocal
    if _SessionLocal is None:
        _SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=get_engine())
    return _SessionLocal


# Keep `engine` as a property-like accessor for backward compat with create_all
class _EngineProxy:
    def __getattr__(self, name):
        return getattr(get_engine(), name)


engine = _EngineProxy()


def get_db():
    SessionLocal = get_session_local()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

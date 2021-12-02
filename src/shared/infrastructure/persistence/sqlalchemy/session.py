import threading
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from shared.infrastructure.logging.file.logger import FileLogger


class ScopedSessionError(RuntimeError):
    pass


class SessionBuilder:
    _sessions = {}
    # _lock = threading.Lock()

    @classmethod
    def build(cls, dsn: str) -> scoped_session:
        if not cls._sessions.get(dsn):
            # with cls._lock:
            if not cls._sessions.get(dsn):
                session_factory = sessionmaker(
                    bind=create_engine(
                        dsn,
                        pool_recycle=500,
                        pool_size=20,
                        max_overflow=0
                    )
                )
                cls._sessions[dsn] = scoped_session(session_factory)
                FileLogger("sqlalchemy.engine")

        return cls._sessions[dsn]


class SessionFactory:
    _safe_session = None

    @classmethod
    def create(cls, dsn: str):
        if not cls._safe_session:
            cls._safe_session = SessionBuilder.build(dsn)

        return cls._safe_session


@contextmanager
def session_scope(dsn: str):
    safe_session = SessionFactory.create(dsn)
    session = safe_session()

    try:
        yield session

        session.commit()
        session.flush()
    except Exception as error:
        session.rollback()

        raise ScopedSessionError(str(error))
    finally:
        # session.close()
        safe_session.remove()

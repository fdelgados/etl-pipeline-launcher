from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

import shared.infrastructure.environment.globalvars as gvars

from shared.infrastructure.logging.file.logger import FileLogger


class ScopedSessionError(RuntimeError):
    pass


class SessionBuilder:
    _sessions = {}

    @classmethod
    def build(cls, dsn: str) -> scoped_session:
        if not cls._sessions.get(dsn):
            if not cls._sessions.get(dsn):
                settings = gvars.settings.environment_settings()
                timeout = settings.get("mariadb").get("wait_timeout")
                session_factory = sessionmaker(
                    bind=create_engine(
                        dsn,
                        pool_recycle=timeout,
                        pool_size=20,
                        max_overflow=0,
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
        safe_session.remove()

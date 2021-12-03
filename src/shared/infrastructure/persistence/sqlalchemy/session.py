from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import shared.infrastructure.environment.globalvars as gvars


class ScopedSessionError(RuntimeError):
    pass


engines = {}
sessions = {}


def init(dsn):
    global engines, sessions

    settings = gvars.settings.environment_settings()
    timeout = settings.get("mariadb").get("wait_timeout")

    engines[dsn] = create_engine(dsn, pool_recycle=timeout)

    sessions[dsn] = sessionmaker(bind=engines[dsn])


@contextmanager
def session_scope(dsn: str):
    global engines, sessions

    init(dsn)

    engine = engines[dsn]
    Session = sessions[dsn]
    session = Session()

    try:
        yield session

        session.commit()
        session.flush()
    except Exception as error:
        session.rollback()

        raise ScopedSessionError(str(error))
    finally:
        session.close()
        engine.dispose()

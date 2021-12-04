from sqlalchemy import text, exc

from shared.infrastructure.persistence.sqlalchemy.session import engines
import shared.infrastructure.environment.globalvars as global_vars
from shared.domain.service.persistence.dbal import (
    DbalService,
    DbalServiceError,
)


class SqlAlchemyDbalService(DbalService):
    def __init__(self, context: str):
        dsn = global_vars.settings.database_dsn(context)
        self._db_engine = engines.get(dsn)

    def execute(self, sentence: str, **parameters):
        with self._db_engine.connect() as connection:
            try:
                return connection.execute(text(sentence), **parameters)
            except exc.SQLAlchemyError as error:
                raise DbalServiceError(str(error))
            finally:
                connection.close()
                self._db_engine.dispose()

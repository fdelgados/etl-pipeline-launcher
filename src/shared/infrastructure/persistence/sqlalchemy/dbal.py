from sqlalchemy import text, exc

from shared.infrastructure.persistence.sqlalchemy.session import engines
from shared.infrastructure.environment.environment import Environment
from shared.domain.service.persistence.dbal import (
    DbalService,
    DbalServiceError,
)


class SqlAlchemyDbalService(DbalService):
    def __init__(self, context: str):
        dsn = Environment.database_dsn(context)
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

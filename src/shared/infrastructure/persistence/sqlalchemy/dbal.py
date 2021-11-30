from sqlalchemy import create_engine, text, exc

from shared.infrastructure.environment.environment import Environment
from shared.domain.service.persistence.dbal import (
    DbalService,
    DbalServiceError,
)


class SqlAlchemyDbalService(DbalService):
    def __init__(self, context: str):
        dsn = Environment.database_dsn(context)
        self._connection = create_engine(dsn, pool_recycle=1)

    def execute(self, sentence: str, **parameters):
        with self._connection.connect() as connection:
            try:
                return connection.execute(text(sentence), **parameters)
            except exc.SQLAlchemyError as error:
                raise DbalServiceError(str(error))
            finally:
                connection.close()

from typing import List, Dict
from sqlalchemy import desc, asc, text

from shared.domain.model.aggregate import AggregateRoot
from shared.domain.model.repository import Repository as BaseRepository

from shared.infrastructure.persistence.sqlalchemy.session import (
    init,
    engines,
    sessions,
    session_scope,
)


class Repository(BaseRepository):
    def __init__(self, aggregate: AggregateRoot, dsn: str):
        self._aggregate = aggregate
        self._dsn = dsn
        init(self._dsn)
        self._session = sessions[self._dsn]
        self._engine = engines[self._dsn]

    def _connection(self):
        return self._engine

    @staticmethod
    def _statement(statement: str):
        return text(statement)

    def add(self, aggregate: AggregateRoot) -> None:
        with session_scope(self._dsn) as session:
            session.add(aggregate)

    def save(self, aggregate: AggregateRoot) -> None:
        with session_scope(self._dsn) as session:
            session.add(aggregate)

    def find(self, **kwargs) -> AggregateRoot:
        session = self._session()

        result = session.query(self._aggregate).filter_by(**kwargs).first()
        session.close()
        self._engine.dispose()

        return result

    def find_all(self, order_by: Dict = None, **kwargs) -> List[AggregateRoot]:
        session = self._session()
        query = session.query(self._aggregate).filter_by(**kwargs)
        if order_by:
            for field, direction in order_by.items():
                if direction == "desc":
                    order_expression = desc(self._aggregate.__dict__[field])
                else:
                    order_expression = asc(self._aggregate.__dict__[field])

                query = query.order_by(order_expression)

        results = query.all()

        session.close()
        self._engine.dispose()

        return results
